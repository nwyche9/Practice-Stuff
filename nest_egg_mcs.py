import sys
import random
import matplotlib.pyplot as plt


def read_to_list(file_name):
    # open a file of percents and convert to decimal then return
    with open(file_name) as in_file:
        lines = [float(line.strip()) for line in in_file]
        decimal = [round(line / 100, 5) for line in lines]
        return decimal


def default_input(prompt, default=None):
    # allow use of default values in input
    prompt = '{} [{}]: '.format(prompt, default)
    response = input(prompt)
    if not response and default:
        return default
    else:
        return response


print("\nNote: Input data should be in percent, not decimal\n")
try:
    bonds = read_to_list('data/10-yr_TBond_returns_1926-2013_pct.txt')
    stocks = read_to_list('data/SP500_returns_1926-2013_pct.txt')
    blend_40_50_10 = read_to_list('data/S-B-C_blend_1926-2013_pct.txt')
    blend_50_50 = read_to_list('data/S-B_blend_1926-2013_pct.txt')
    inflation_rate = read_to_list('data/annual_infl_rate_1926-2013_pct.txt')
    gold = read_to_list('data/gold_pct_growth.txt')

except IOError as e:
    print("{}. \n Terminating program.".format(e), file=sys.stderr)
    sys.exit(1)

investment_type_args = {'bonds': bonds, 'stocks': stocks, 'sb_blend': blend_50_50, 'sbc_blend': blend_40_50_10, 'gold': gold}

print(" stocks = SP500")
print(" bonds = 10-yr Treasury Bond")
print(" sb_blend = 50% SP500/ 50% TBond")
print(" sbc_blend = 40% SP500/ 50% TBond/ 10% Cash")
print(" good old gold\n")
#print(" sg_blend = 50% SP500/ 50% Gold\n")
#print(" sbg_blend = 40% SP500/ 50% TBond/ 10% Gold\n")
#print(" Or your own blend\n")
print("Press ENTER to take default value shown in [brackets]. \n")

invest_type = default_input("Enter investment type: (stocks, bonds, sb_blend, sbc_blend,  gold): \n", 'bonds').lower()

while invest_type not in investment_type_args:
    invest_type = input("Invalid investment. Enter investment type as listed in prompt: ")

start_value = default_input("Input starting value of investments: \n", '2000000')

while not start_value.isdigit():
    start_value = input("Invalid input! Input integer only: ")

withdrawal = default_input("Input annual pre-tax withdrawal (today's $): \n", '80000')

while not withdrawal.isdigit():
    withdrawal = input("Invalid input! Input integer only: ")

min_years = default_input("Input minimum years in retirement: \n", '18')
while not min_years.isdigit():
    min_years = input("Invalid input! Input integer only: ")

most_likely_years = default_input("Input most-likely years in retirement: \n", '25')
while not most_likely_years.isdigit():
    most_likely_years = input("Invalid input! Input integer only: ")

max_years = default_input("Input the maximum years in retirement: \n", '40')
while not max_years.isdigit():
    max_years = input("Invalid input! Input integer only: ")

num_cases = default_input("Input number of cases to run: \n", '50000')
while not num_cases.isdigit():
    num_cases = input("Invalid input! Input integer only: ")

if not int(min_years) < int(most_likely_years) < int(max_years) or int(max_years) > 99:
    print("\nProblem with input years.", file=sys.stderr)
    print("Requires Min < Most_Likely < Max with Max <= 99.", file=sys.stderr)
    sys.exit(1)


def montecarlo(returns):
    case_count = 0  # keep track of specific case
    bankrupt_count = 0
    outcome = []

    while case_count < int(num_cases):
        investments = int(start_value)
        start_year = random.randrange(0, len(returns))
        duration = int(random.triangular(int(min_years), int(max_years), int(most_likely_years)))
        end_year = start_year + duration
        lifespan = [i for i in range(start_year, end_year)]
        bankrupt = 'no'

        lifespan_returns = []
        lifespan_inflation = []
        for i in lifespan:
            lifespan_returns.append(returns[i % len(
                returns)])  # since the retirement may last past 2013, must wrap around to 1926 and start again
            lifespan_inflation.append(inflation_rate[i % len(inflation_rate)])

        for index, i in enumerate(lifespan_returns):
            inflation = lifespan_inflation[index]

            if index == 0:
                withdraw_inflation_adjusted = int(withdrawal)
            else:
                withdraw_inflation_adjusted = int(withdraw_inflation_adjusted * (1 + inflation))

            investments -= withdraw_inflation_adjusted
            investments = int(investments * (1 + i))

            if investments <= 0:
                bankrupt = 'yes'
                break

        if bankrupt == 'yes':
            outcome.append(0)
            bankrupt_count += 1
        else:
            outcome.append(investments)
            case_count += 1

    return outcome, bankrupt_count


def bankrupt_probability(outcome, bankrupt_count):
    total = len(outcome)
    odds = round(100 * bankrupt_count / total, 1)

    print("\nInvestment type: {}".format(invest_type))
    print("Starting value: ${:,}".format(int(start_value)))
    print("Annual withdrawal: ${:,}".format(int(withdrawal)))
    print("Years in retirement (min-ml-max): {}-{}-{}".format(min_years, most_likely_years, max_years))
    print("Number of runs: {:,}\n".format(len(outcome)))
    print("Odds of running out of money: {}%\n".format(odds))
    print("Average outcome: ${:,}".format(int(sum(outcome) / total)))
    print("Minimum outcome: ${:,}".format(min(i for i in outcome)))
    print("Maximum outcome: ${:,}".format(max(i for i in outcome)))

    return odds


def main():
    outcome, bankrupt_count = montecarlo(investment_type_args[invest_type])
    odds = bankrupt_probability(outcome, bankrupt_count)

    plotdata = outcome[:3000]
    plotdata.sort()

    plt.figure('Outcome by Case (showing first {} runs)'.format(len(plotdata)), figsize=(16, 5))
    index = [i + 1 for i in range(len(plotdata))]
    plt.bar(index, plotdata, color='black')
    plt.xlabel('Simulated Lives', fontsize=18)
    plt.ylabel('$ Remaining', fontsize=18)
    plt.ticklabel_format(style='plain', axis='y')
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    plt.title('Probability of running out of money = {}%'.format(odds), fontsize=20, color='red')
    plt.show()


if __name__ == '__main__':
    main()
