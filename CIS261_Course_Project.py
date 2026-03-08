# ********************************************************
# Name: Bryan Peterson
# Class: CIS261
# Lab: Course Project Phase 4
# ********************************************************

from datetime import datetime

def CreateUsers():
    print("##### Create users, passwords, and roles #####")
    # Open the file so data is appended, not overwritten
    UserFile = open("Users.txt", "a+")
    
    # Read existing user IDs into a list for validation
    UserFile.seek(0)
    user_ids = []
    for line in UserFile:
        line = line.replace("\n", "")
        if not line:
            continue
        parts = line.split("|")
        if parts:
            user_ids.append(parts[0])
    # Move pointer to end for appending new users
    UserFile.seek(0, 2)

    while True:
        username = GetUserName()
        if username.upper() == "END":
            break

        # Make sure user ID is unique
        if username in user_ids:
            print("User ID already exists. Please enter a different user name.\n")
            continue

        userpwd = GetUserPassword()
        userrole = GetUserRole()
        UserDetail = username + "|" + userpwd + "|" + userrole + "\n"
        UserFile.write(UserDetail)
        user_ids.append(username)
        print(f"User {username} with role {userrole} added.\n")

    UserFile.close()


def GetUserName():
    username = input("Enter user name or 'End' to quit: ")
    return username


def GetUserPassword():
    pwd = input("Enter password: ")
    return pwd


def GetUserRole():
    userrole = input("Enter role (Admin or User): ")
    while True:
        if userrole.upper() == "ADMIN" or userrole.upper() == "USER":
            return userrole
        else:
            userrole = input("Enter role (Admin or User): ")


def printuserinfo():
    print("\n##### Current Users #####")
    try:
        UserFile = open("Users.txt", "r")
    except FileNotFoundError:
        print("No user file found yet.\n")
        return

    while True:
        UserDetail = UserFile.readline()
        if not UserDetail:
            break
        UserDetail = UserDetail.replace("\n", "")  # remove carriage return
        UserList = UserDetail.split("|")
        username = UserList[0]
        userpassword = UserList[1]
        userrole = UserList[2]
        print("User Name:", username, " Password:", userpassword, " Role:", userrole)

    UserFile.close()
    print("---------------------------\n")


def Login():
    # read login information and store in a list
    try:
        UserFile = open("Users.txt", "r")
    except FileNotFoundError:
        print("User file not found. Please create users first.")
        return "NONE", ""

    UserName = input("Enter User Name: ")
    UserRole = "None"

    # Optional: you could also prompt for password and validate it here
    # pwd_input = input("Enter Password: ")

    while True:
        UserDetail = UserFile.readline()
        if not UserDetail:
            UserFile.close()
            return UserRole, UserName

        UserDetail = UserDetail.replace("\n", "")
        UserList = UserDetail.split("|")
        if UserName == UserList[0]:
            # If you wanted password checking, UserList[1] is the stored password
            UserRole = UserList[2]  # user is valid, return role
            UserFile.close()
            return UserRole, UserName

    UserFile.close()
    return UserRole, UserName


def GetEmpName():
    empname = input("Enter employee name (or 'End' to quit): ")
    return empname


def GetDatesWorked():
    fromdate = input("Enter Start Date (mm/dd/yyyy): ")
    todate = input("Enter End Date (mm/dd/yyyy): ")
    return fromdate, todate


def GetHoursWorked():
    hours = float(input("Enter amount of hours worked: "))
    return hours


def GetHourlyRate():
    hourlyrate = float(input("Enter hourly rate: "))
    return hourlyrate


def GetTaxRate():
    taxrate = float(input("Enter tax rate (e.g., 0.2 for 20%): "))
    return taxrate


def CalcTaxAndNetPay(hours, hourlyrate, taxrate):
    grosspay = hours * hourlyrate
    incometax = grosspay * taxrate
    netpay = grosspay - incometax
    return grosspay, incometax, netpay


def printinfo(DetailsPrinted, EmpTotals):
    TotEmployees = 0
    TotHours = 0.00
    TotGrossPay = 0.00
    TotTax = 0.00
    TotNetPay = 0.00

    try:
        EmpFile = open("Employees.txt", "r")
    except FileNotFoundError:
        print("No employee data file found yet.\n")
        return

    # Ask for report date filter
    while True:
        rundate = input(
            "Enter start date for report (MM/DD/YYYY) or All for all data in file: "
        )
        if rundate.upper() == "ALL":
            break
        try:
            rundate_dt = datetime.strptime(rundate, "%m/%d/%Y")
            break
        except ValueError:
            print("Invalid date format. Try again.\n")
            continue

    while True:
        EmpDetail = EmpFile.readline()
        if not EmpDetail:
            break
        EmpDetail = EmpDetail.replace("\n", "")  # remove carriage return
        EmpList = EmpDetail.split("|")
        fromdate = EmpList[0]

        # Filter by date if not "All"
        if rundate.upper() != "ALL":
            checkdate = datetime.strptime(fromdate, "%m/%d/%Y")
            if checkdate < rundate_dt:
                continue

        todate = EmpList[1]
        empname = EmpList[2]
        hours = float(EmpList[3])
        hourlyrate = float(EmpList[4])
        taxrate = float(EmpList[5])
        grosspay, incometax, netpay = CalcTaxAndNetPay(hours, hourlyrate, taxrate)

        print(
            fromdate,
            todate,
            empname,
            f"{hours:,.2f}",
            f"{hourlyrate:,.2f}",
            f"{grosspay:,.2f}",
            f"{taxrate:,.1%}",
            f"{incometax:,.2f}",
            f"{netpay:,.2f}",
        )

        TotEmployees += 1
        TotHours += hours
        TotGrossPay += grosspay
        TotTax += incometax
        TotNetPay += netpay

        EmpTotals["TotEmp"] = TotEmployees
        EmpTotals["TotHrs"] = TotHours
        EmpTotals["TotGrossPay"] = TotGrossPay
        EmpTotals["TotTax"] = TotTax
        EmpTotals["TotNetPay"] = TotNetPay
        DetailsPrinted = True

    EmpFile.close()

    if DetailsPrinted:
        PrintTotals(EmpTotals)
    else:
        print("No detail information to print.")


def PrintTotals(EmpTotals):
    print()
    print(f"Total Number Of Employees: {EmpTotals['TotEmp']}")
    print(f"Total Hours Worked: {EmpTotals['TotHrs']:,.2f}")
    print(f"Total Gross Pay: {EmpTotals['TotGrossPay']:,.2f}")
    print(f"Total Income Tax: {EmpTotals['TotTax']:,.2f}")
    print(f"Total Net Pay: {EmpTotals['TotNetPay']:,.2f}")
    print()


def main():
    # 1) Create users and store them in Users.txt
    CreateUsers()

    # 2) Show user login info (for screenshot requirement)
    printuserinfo()

    print("##### Data Entry #####")
    DetailsPrinted = False
    EmpTotals = {}

    # 3) Login
    UserRole, UserName = Login()

    if UserRole.upper() == "NONE":
        print(UserName, "is invalid.")
    else:
        print(f"Login successful. User: {UserName}, Role: {UserRole}")
        print()

        # Only Admin users can enter data
        if UserRole.upper() == "ADMIN":
            EmpFile = open("Employees.txt", "a+")
            while True:
                empname = GetEmpName()
                if empname.upper() == "END":
                    break
                fromdate, todate = GetDatesWorked()
                hours = GetHoursWorked()
                hourlyrate = GetHourlyRate()
                taxrate = GetTaxRate()
                EmpDetail = (
                    fromdate
                    + "|"
                    + todate
                    + "|"
                    + empname
                    + "|"
                    + str(hours)
                    + "|"
                    + str(hourlyrate)
                    + "|"
                    + str(taxrate)
                    + "\n"
                )
                EmpFile.write(EmpDetail)
            # close file to save data
            EmpFile.close()

            # Admin can display detail and totals
            printinfo(DetailsPrinted, EmpTotals)

        else:
            # User role: display-only access
            print("You have 'User' access (display only).")
            printinfo(DetailsPrinted, EmpTotals)


if __name__ == "__main__":
    main()