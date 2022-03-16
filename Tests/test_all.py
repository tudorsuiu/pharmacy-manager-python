from Tests.test_domain import test_domain
from Tests.test_repository import test_repository
from Tests.test_service import test_service
from Tests.test_undo_redo import test_undo_redo


def test_all():
    test_domain()
    test_repository()
    test_service()
    test_undo_redo()
