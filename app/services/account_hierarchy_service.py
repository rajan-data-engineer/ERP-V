from sqlmodel import Session, select
from typing import Dict, List, Optional

from app.models.account import Account
from app.models.ledger import LedgerEntry


class AccountHierarchyService:

    # --------------------------------------------------
    # BUILD RAW ACCOUNT TREE (MULTI-LEVEL)
    # --------------------------------------------------
    @staticmethod
    def build_tree(session: Session) -> List[Dict]:
        accounts = session.exec(select(Account)).all()

        # Index by ID for fast lookup
        account_map = {acc.id: acc for acc in accounts}

        # Child mapping
        children_map = {}
        for acc in accounts:
            parent = acc.parent_id
            children_map.setdefault(parent, []).append(acc)

        # Build tree from root accounts (parent_id = None)
        def build_node(account: Account):
            return {
                "id": account.id,
                "code": account.code,
                "name": account.name,
                "type": account.type,
                "children": [
                    build_node(child)
                    for child in children_map.get(account.id, [])
                ]
            }

        roots = children_map.get(None, [])
        return [build_node(acc) for acc in roots]

    # --------------------------------------------------
    # CALCULATE BALANCES RECURSIVELY
    # --------------------------------------------------
    @staticmethod
    def calculate_rollup_balances(session: Session) -> Dict[int, float]:
        accounts = session.exec(select(Account)).all()
        ledger = session.exec(select(LedgerEntry)).all()

        # Start with zero balance
        balance_map = {acc.id: 0.0 for acc in accounts}

        # Apply ledger entries to accounts
        for entry in ledger:
            if entry.account_id in balance_map:
                balance_map[entry.account_id] += entry.debit - entry.credit

        # Roll up from children to parent accounts
        accounts_by_parent = {}
        for acc in accounts:
            accounts_by_parent.setdefault(acc.parent_id, []).append(acc)

        def rollup(acc_id: int) -> float:
            total = balance_map[acc_id]

            # Add balances of all children
            for child in accounts_by_parent.get(acc_id, []):
                total += rollup(child.id)

            return total

        # Final rollup results
        final_balances = {}
        for acc in accounts:
            final_balances[acc.id] = rollup(acc.id)

        return final_balances

    # --------------------------------------------------
    # BUILD FULL TREE WITH ROLLUP BALANCES
    # --------------------------------------------------
    @staticmethod
    def build_tree_with_balances(session: Session) -> List[Dict]:
        accounts = session.exec(select(Account)).all()
        balances = AccountHierarchyService.calculate_rollup_balances(session)

        children_map = {}
        for acc in accounts:
            children_map.setdefault(acc.parent_id, []).append(acc)

        def build_node(acc: Account):
            return {
                "id": acc.id,
                "code": acc.code,
                "name": acc.name,
                "type": acc.type,
                "balance": balances[acc.id],
                "children": [
                    build_node(child)
                    for child in children_map.get(acc.id, [])
                ]
            }

        roots = children_map.get(None, [])
        return [build_node(acc) for acc in roots]
