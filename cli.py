import decimal
from datetime import datetime

from database import connect_to_db
from utils import (
    fetch_budgets_for_current_month,
    notification_sent_for_month,
    send_notification,
    set_shop_offline,
)


def get_current_month():
    if "__testdb" in connect_to_db().database:
        return "2023-02-01"
    return datetime.now().strftime("%Y-%m-01")


def check_budgets():
    # Fetch the budget and amount spent for each shop for the current month
    current_month = get_current_month()
    budgets = fetch_budgets_for_current_month(current_month)
    flag = False
    if budgets:
        # Loop through each budget
        for (
            shop_id,
            budget,
            spent,
            notification_sent,
            notification_current_threshold,
        ) in budgets:
            # Check if the amount spent has reached 50% of the budget
            budget_check_amount = budget * decimal.Decimal(0.5)
            if spent >= budget_check_amount:
                # If notifications have not been sent for this shop and month, send a notification and mark it as sent
                if not notification_sent_for_month(notification_sent):
                    notification = send_notification(
                        shop_id,
                        budget,
                        spent,
                        0.5,
                        notification_current_threshold,
                        current_month,
                    )
                    if notification:
                        flag = True

            # Check if the amount spent has reached 100% of the budget
            if spent >= budget:
                # If notifications have not been sent for this shop and month, send a notification and mark it as sent
                if not notification_sent_for_month(notification_sent):
                    notification = send_notification(
                        shop_id,
                        budget,
                        spent,
                        1.0,
                        notification_current_threshold,
                        current_month,
                    )
                    set_shop_offline(shop_id)
                    if notification:
                        flag = True
        if not flag:
            print("No budget found!")
    else:
        print("No data found!")


def main():
    check_budgets()


if __name__ == "__main__":
    # calling the main function
    main()
