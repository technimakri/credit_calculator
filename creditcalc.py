import argparse, math, string, sys

parser = argparse.ArgumentParser()
parser.add_argument("--type", help="Choose type of loan, annuity or differentiated")
parser.add_argument("--principal", type=int, help="Enter the prinicipal loan amount")
parser.add_argument("--interest", type=float, help="Enter the interest rate as a percentage without a '%' sign e.g. '10'")
parser.add_argument("--periods", type=int, help="Enter the count of periods that the loan will be repaid over")
parser.add_argument("--payment", type=int, help="Enter the annuity payment amount each month")
args = parser.parse_args()

# Input validation
def incorrect():
    print("Incorrect parameters")
    sys.exit()

if args.type not in ["diff", "annuity"]:
    incorrect()
if args.type == "diff" and args.payment:
    incorrect()
if args.interest == None:
    incorrect()
if len([arg for arg in vars(args).values() if arg == None]) > 1:
    incorrect()
if any([arg for arg in vars(args) if type(arg) == int and arg < 0]):
    incorrect()

# Short form of variables used in calculations
a = args.payment
p = args.principal
n = args.periods
i = args.interest / 12 / 100

# Calculation functions
def print_overpay(calc):
    print(f"Overpayment = {calc}")

def annuity_payment():
    annuity_payment = math.ceil(p * ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))
    ann_overpay = annuity_payment * n - p
    print(f"Your annuity payment = {annuity_payment}!")
    print_overpay(ann_overpay)

def credit_principal():
    credit_principal = math.floor(a / ((i * (1 + i) ** n) / ((1 + i) ** n - 1)))
    princ_overpay = a * n - credit_principal
    print(f"Your credit principal = {credit_principal}!")
    print_overpay(princ_overpay)

def number_payments():
    number_payments = math.ceil(math.log(a / (a - i * p), 1 + i))
    years = number_payments // 12
    years_plural = True if years > 1 else None
    months = number_payments % 12
    months_plural = True if months > 1 else None
    num_overpay = number_payments * a - p
    print("You need ",
          f"{years if years else ''}",
          f"{' year' if years else ''}" + f"{'s' if years_plural else ''}",
          f"{' and ' if years and months else ''}",
          f"{months if months else ''}",
          f"{' month' if months else ''}" + f"{'s' if months_plural else ''}",
          " to repay this credit!", sep="")
    print_overpay(num_overpay)

def diff_payment():
    payment_list = [math.ceil(p / n + i * (p - ((p * (m - 1)) / n))) for m in range(1, n + 1)]
    diff_overpay = sum(payment_list) - p
    for count, payment in enumerate(payment_list):
        print(f"Month {count + 1}: paid out {payment}")
    print_overpay(diff_overpay)

# User selection logic
if args.type == "diff" and all([p, n, i]):
    diff_payment()
if args.type == "annuity":
    if all([p, n, i]):
        annuity_payment()
    if p == None:
        credit_principal()
    if n == None:
        number_payments()
