from domain.services.dashboard_service import DashboardService


def test_dashboard_kpis_empty(db_session):
    svc = DashboardService(db_session)
    k = svc.kpis()
    assert isinstance(k, dict)
