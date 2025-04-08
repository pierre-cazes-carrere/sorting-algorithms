
from interface.interface_dark import SortingAppWithSeaborn
import customtkinter as ctk

if __name__ == "__main__":
    root = ctk.CTk()
    app = SortingAppWithSeaborn(root)
    root.mainloop()
