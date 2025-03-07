from superqt.qtcompat.QtCore import Qt
from superqt.spinbox import QLargeIntSpinBox


def test_large_spinbox(qtbot):
    sb = QLargeIntSpinBox()
    qtbot.addWidget(sb)

    for e in range(2, 100, 2):
        sb.setMaximum(10 ** e + 2)
        with qtbot.waitSignal(sb.valueChanged) as sgnl:
            sb.setValue(10 ** e)
        assert sgnl.args == [10 ** e]
        assert sb.value() == 10 ** e

        sb.setMinimum(-(10 ** e) - 2)

        with qtbot.waitSignal(sb.valueChanged) as sgnl:
            sb.setValue(-(10 ** e))
        assert sgnl.args == [-(10 ** e)]
        assert sb.value() == -(10 ** e)


def test_large_spinbox_type(qtbot):
    sb = QLargeIntSpinBox()
    qtbot.addWidget(sb)

    assert isinstance(sb.value(), int)

    sb.setValue(1.1)
    assert isinstance(sb.value(), int)
    assert sb.value() == 1

    sb.setValue(1.9)
    assert isinstance(sb.value(), int)
    assert sb.value() == 1


def test_large_spinbox_signals(qtbot):
    sb = QLargeIntSpinBox()
    qtbot.addWidget(sb)

    with qtbot.waitSignal(sb.valueChanged) as sgnl:
        sb.setValue(200)
    assert sgnl.args == [200]

    with qtbot.waitSignal(sb.textChanged) as sgnl:
        sb.setValue(240)
    assert sgnl.args == ["240"]


def test_keyboard_tracking(qtbot):
    sb = QLargeIntSpinBox()
    qtbot.addWidget(sb)

    assert sb.value() == 0
    sb.setKeyboardTracking(False)
    with qtbot.assertNotEmitted(sb.valueChanged):
        sb.lineEdit().setText("20")
    assert sb.lineEdit().text() == "20"
    assert sb.value() == 0
    assert sb._pending_emit is True

    with qtbot.waitSignal(sb.valueChanged) as sgnl:
        qtbot.keyPress(sb, Qt.Key.Key_Enter)
    assert sgnl.args == [20]
    assert sb._pending_emit is False

    sb.setKeyboardTracking(True)
    with qtbot.waitSignal(sb.valueChanged) as sgnl:
        sb.lineEdit().setText("25")
    assert sb._pending_emit is False
    assert sgnl.args == [25]
