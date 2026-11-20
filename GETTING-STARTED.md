# Getting started

How to get the Miko project onto a new computer and open it in your browser. You don't need to know anything about programming for this. It takes about 30 minutes, most of it waiting for downloads.

At the end you have the Miko pages open at **http://localhost:5067**, and every change you save shows up in the browser.

This guide is for Windows. On a Mac it works the same, apart from the lines marked **Mac**.

## 1. Install three programs (only once)

| Program | What it is for |
|---|---|
| GitHub Desktop | gets the project onto your computer and sends your changes back to the team |
| .NET 10 SDK | runs the project |
| Visual Studio Code | where you open and change the files |

### GitHub Desktop

1. Make an account on [github.com](https://github.com) if you don't have one yet.
2. Send your GitHub username to Hugo, so he can add you to the project. Without that you can still download it, but you can't send your changes back.
3. Download GitHub Desktop from [desktop.github.com](https://desktop.github.com), install it and sign in with your GitHub account.

### .NET 10 SDK

1. Go to [dotnet.microsoft.com/download/dotnet/10.0](https://dotnet.microsoft.com/download/dotnet/10.0).
2. In the **SDK** column, click **Windows x64** under Installers. Take the SDK, not the Runtime.
   **Mac:** pick macOS **Arm64** for a Mac with an M chip, **x64** for an older Intel Mac.
3. Open the file you downloaded and click through the installer.
4. Check that it worked: press the Windows key, type **PowerShell** and open it. Type this and press Enter:

   ```
   dotnet --list-sdks
   ```

   You should see a line that starts with `10.0`. Close PowerShell again.
   **Mac:** use the Terminal app instead of PowerShell.

### Visual Studio Code

1. Download it from [code.visualstudio.com](https://code.visualstudio.com) and install it. The default options are fine.

## 2. Get the project

1. Open GitHub Desktop. Click **File**, then **Clone repository**, then the **URL** tab.
2. Paste this address:

   ```
   https://github.com/hugoantonrigholt/EN14-C3
   ```

3. At **Local path**, pick a folder you can find back, like `Documents\GitHub\EN14-C3`. Don't pick a OneDrive or iCloud folder: they lock files while they sync, and then the project won't start.
4. Click **Clone** and wait until it's done.
5. Pick the branch you work on: click **Current branch** at the top and choose it. For the pages that is **Features/FrontEndFiles** (until it is merged into main).

## 3. Run it in the browser

1. In GitHub Desktop, click **Repository**, then **Open in Visual Studio Code**.
   If it offers a different editor: **File**, **Options**, **Integrations**, set External editor to Visual Studio Code, and try again.
2. In VS Code, click **Terminal** in the menu at the top, then **New Terminal**. A panel opens at the bottom, already in the project folder.
3. Type this and press Enter:

   ```
   dotnet watch
   ```

   The first time it downloads what the project needs, that takes a minute.
4. Wait until you see a line like `Now listening on: http://localhost:5067`.
5. Open your browser and go to **http://localhost:5067**. You see the Dashboard with the menu on the left.

Leave the terminal running while you work. Save a `.cshtml` or `.css` file (Ctrl+S, **Mac:** Cmd+S), then press F5 in the browser to see the change. The first save after starting can take up to a minute, after that it's about a second.

- If the terminal asks **"Do you want to restart your app?"**, press **a** (always).
- To stop it, click in the terminal and press **Ctrl+C**.
- Next time you only do step 3: open the project in VS Code, open a terminal, `dotnet watch`.

What to do in the pages themselves is in [FRONTEND.md](FRONTEND.md).

## 4. Every time you work on it

1. **Before you start:** in GitHub Desktop, click **Fetch origin**, then **Pull origin** if it shows up. Now you have what the others sent.
2. **While you work:** run it as in step 3.
3. **When something works:** GitHub Desktop shows the files you changed. Write a short summary at the bottom left (like "Scan page: live view and button"), click **Commit**, then **Push origin**. Now the others can get it.

Commit small and often, not once at the end of the week.

## 5. The database (not needed for the pages yet)

The pages run without it. You only need it once the pages show real data, and it only works on Windows.

1. Install **SQL Server Express LocalDB**: go to [microsoft.com/sql-server/sql-server-downloads](https://www.microsoft.com/sql-server/sql-server-downloads), download **Express** and choose **LocalDB** in the installer. Check it in PowerShell with `sqllocaldb info`, it should say `MSSQLLocalDB`.
2. In the VS Code terminal, install the database tool once:

   ```
   dotnet tool install --global dotnet-ef
   ```

3. Make the Miko database:

   ```
   dotnet ef database update
   ```

**Mac:** LocalDB doesn't exist on a Mac. Ask Marcos, it needs SQL Server in Docker and a different connection string.

## When something goes wrong

| You see | Do this |
|---|---|
| `dotnet` is not recognized, or command not found | Close the terminal and open a new one. Still there? Restart the computer. Still there? Install the .NET 10 SDK again. |
| `NETSDK1045` ... does not support targeting .NET 10.0 | You have an older .NET. Install the .NET 10 SDK (step 1). |
| Couldn't find a project to run | The terminal is in the wrong folder. In VS Code, **File**, **Open Folder**, pick the `EN14-C3` folder (the one with `Program.cs` in it) and open a new terminal. |
| Address already in use, or Failed to bind to address | `dotnet watch` is already running in another terminal. Stop that one with Ctrl+C, or close VS Code and start again. |
| This site can't be reached | `dotnet watch` isn't running, or it hasn't finished starting. Look at the terminal. |
| "This localhost page can't be found" (404) | You are on a branch without the pages. In GitHub Desktop, **Current branch**, pick Features/FrontEndFiles. |
| You saved, but the page didn't change | Is `dotnet watch` still running? Press F5, or Ctrl+F5 after a CSS change. Right after starting, the first change can take up to a minute. |

Still stuck? Copy the red text from the terminal and send it to Hugo or Marcos.
