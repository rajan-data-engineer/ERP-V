def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=getattr(settings, "VERSION", "1.0.0")
    )

    # ----------------------------------------------------
    # STATIC FILES (Excel Exports)
    # ----------------------------------------------------
    app.mount("/exports", StaticFiles(directory="app/exports"), name="exports")

    # ----------------------------------------------------
    # CORS (Allow All for Now)
    # ----------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ----------------------------------------------------
    # ROUTERS
    # ----------------------------------------------------
    app.include_router(auth_router)
    app.include_router(admin_router)
    app.include_router(account_router)
    app.include_router(journal_router)
    app.include_router(ledger_router)
    app.include_router(products_router)
    app.include_router(inventory_router)
    app.include_router(customers_router)
    app.include_router(sales_router)
    app.include_router(dashboard_router)
    app.include_router(fiscal_router)
    app.include_router(account_tree_router)
    app.include_router(audit_router)
    app.include_router(export_router)

    # ----------------------------------------------------
    # STARTUP — CREATE TABLES + BOOTSTRAP ADMIN
    # ----------------------------------------------------
    @app.on_event("startup")
    def on_startup():
        print("Initializing ERP-V database...")
        SQLModel.metadata.create_all(engine)
        print("Database initialized successfully.")

        # Bootstrap admin (runs only once)
        with Session(engine) as session:
            admin_exists = session.exec(
                select(User).where(User.role == "admin")
            ).first()

            if admin_exists:
                print("Admin already exists. Skipping bootstrap.")
                return

            user = session.exec(
                select(User).where(User.username == "RajanShelke")
            ).first()

            if user:
                user.role = "admin"
                user.is_active = True
                session.add(user)
                session.commit()
                print("✅ Bootstrap admin user: RajanShelke")
            else:
                print("⚠️ Bootstrap skipped: user 'RajanShelke' not found")

    # ----------------------------------------------------
    # ROOT ENDPOINT
    # ----------------------------------------------------
    @app.get("/")
    def root():
        return {
            "status": "ok",
            "message": f"{settings.PROJECT_NAME} Backend Running",
            "version": getattr(settings, "VERSION", "1.0.0")
        }

    return app


app = create_app()
