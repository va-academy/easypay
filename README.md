# EasyPay.

A beginner-friendly Python finance tracker for practicing Git and GitHub...
Use fictional data: this application records income and expenses locally and
does not process real payments...

## Run the app

Install Python 3, then run this command from the project folder:

```powershell
py pay.py
```

If your system uses the `python` command instead, run `python pay.py`.
There are no third-party dependencies.

The menu lets you add income, add expenses, view your balance, and list your
transaction history. Amounts are in INR with up to two decimal places.
Transactions are saved beside the script in `transactions.json`. This file is
excluded from Git so your local financial entries are not committed.

## Practice Git and GitHub

Initialize the repository and make your first commit:

```powershell
git init
git add pay.py README.md .gitignore
git commit -m "Add EasyPay finance tracker"
git branch -M main
```

Create an empty repository on GitHub (without a README or license), then
replace YOUR-USERNAME in this command with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/EasyPay.git
git push -u origin main
```

Try a small feature on a new branch, such as adding expense categories:

```powershell
git switch -c feature/expense-categories
```

Edit the code, run the app to check it, then review and commit your changes:

```powershell
git diff
git add pay.py
git commit -m "Add expense categories"
git push -u origin feature/expense-categories
```

Open a pull request on GitHub to compare your branch with `main`. After merging
the pull request, update your local copy:

```powershell
git switch main
git pull
git log --oneline
```
