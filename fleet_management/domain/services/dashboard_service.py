from sqlalchemy import func


class DashboardService:
    def __init__(self, db_session):
        self.db = db_session

    def kpis(self):
        # returns a dict with basic counts
        result = {}
        result['total_transporters'] = self.db.execute(func.count().select().select_from('transporters')).scalar() if False else None
        # Fallback: query tables via SQLAlchemy text for portability
        try:
            res = self.db.execute('SELECT COUNT(*) FROM transporters')
            result['total_transporters'] = res.scalar_one()
        except Exception:
            result['total_transporters'] = 0

        try:
            res = self.db.execute('SELECT COUNT(*) FROM vehicles')
            result['total_vehicles'] = res.scalar_one()
        except Exception:
            result['total_vehicles'] = 0

        try:
            res = self.db.execute('SELECT COUNT(*) FROM drivers')
            result['total_drivers'] = res.scalar_one()
        except Exception:
            result['total_drivers'] = 0

        try:
            res = self.db.execute("SELECT COUNT(*) FROM trips")
            result['total_trips'] = res.scalar_one()
        except Exception:
            result['total_trips'] = 0

        try:
            res = self.db.execute("SELECT COUNT(*) FROM maintenances WHERE status='aberto'")
            result['maintenances_open'] = res.scalar_one()
        except Exception:
            result['maintenances_open'] = 0

        try:
            res = self.db.execute("SELECT COUNT(*) FROM documents WHERE data_vencimento <= date('now','+30 day')")
            result['documents_expiring_30d'] = res.scalar_one()
        except Exception:
            result['documents_expiring_30d'] = 0

        try:
            res = self.db.execute('SELECT IFNULL(SUM(valor_total),0) FROM fuelings')
            result['fuel_cost_total'] = res.scalar_one()
        except Exception:
            # SQLite uses coalesce
            try:
                res = self.db.execute('SELECT COALESCE(SUM(valor_total),0) FROM fuelings')
                result['fuel_cost_total'] = res.scalar_one()
            except Exception:
                result['fuel_cost_total'] = 0

        return result
