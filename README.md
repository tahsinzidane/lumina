**Lumina** is a lightweight, aesthetic shell wrapper built with Python. It enhances your terminal experience by providing **fish-style ghost text suggestions** based on your command history, stored locally in a JSON database.



## 🚀 Features

* **Ghost Text Suggestions:** Real-time, inline command suggestions as you type.
* **Persistent History:** Commands are saved in a local JSON file and persist across sessions.
* **Intelligent Directory Tracking:** Unlike standard subprocess wrappers, Lumina handles `cd` commands internally to maintain your current working directory.
* **Aesthetic UI:** Minimalist prompt design with a focus on readability and "Gen Z" aesthetics.
* **Modular Architecture:** Clean separation of concerns between storage, logic, and execution.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tahsinzidane/lumina.git
   cd Lumina
   ```

2. **Run the installer:**
   The included `install.sh` will set up the project and create a global `lumina` command.
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Reload your shell:**
   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

## ⌨️ Usage

Simply type `lumina` in your terminal to start the wrapper.

```bash
lumina
```

* **Accept Suggestion:** Press the **Right Arrow (→)** or **End** key.
* **Exit:** Type `exit` or `quit` to return to your default shell.

## 📂 Project Structure

```text
Lumina/
├── main.py            # Entry point & Command Loop
├── install.sh         # System-wide installation script
├── core/              
│   ├── __init__.py    # Package initializer
│   ├── suggester.py   # Ghost text & Logic engine
│   └── storage.py     # JSON Persistence layer
└── .gitignore         # Ignores bytecode and local history
```

## 🤝 Contributing

This is a personal project, but contributions are absolutely welcome! 
* If you find a bug, please **create an issue**.
* If you want to add a feature, feel free to **submit a pull request**.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---
