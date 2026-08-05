"""Application entry point."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from benford_lens.ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900, 700)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
