from database import connect_to_db


def fetch_budgets_for_current_month(current_month):
    # Create a cursor
    conn = connect_to_db()
    cursor = conn.cursor()

    # Execute a SQL query to fetch the budgets for the current month for online shops only
    cursor.execute(
        """
            SELECT t_budgets.a_shop_id, t_budgets.a_budget_amount, t_budgets.a_amount_spent, t_budgets.a_notification_sent, 
            t_budgets.a_notification_current_threshold
            FROM t_budgets
            JOIN t_shops ON t_budgets.a_shop_id = t_shops.a_id
            WHERE t_budgets.a_month = %s AND t_shops.a_online = True
        """,
        (current_month,),
    )

    # Fetch the results
    budgets = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()

    # Return the budgets
    return budgets


def send_notification(shop_id, spent, budget, threshold, last_threshold, current_month):
    """
    Send notification if the shop has spent more than its budget and the current threshold is different from the last.
    Return True if a notification was sent, False otherwise.
    """
    if spent >= budget and threshold != last_threshold:
        message = f"Attention! Shop with id {shop_id} has reached {threshold * 100}% of its budget for the current month."

        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute(
            """
               UPDATE t_budgets
               SET a_notification_current_threshold = %s
               WHERE a_shop_id = %s AND a_month = %s
            """,
            (threshold, shop_id, current_month),
        )

        conn.commit()
        cursor.close()

        # Print notification
        print(message)

        mark_notification_sent(shop_id, current_month)

        return True
    return False


def notification_sent_for_month(notification_send):
    """Return True if a notification has been sent for the month, False otherwise."""
    return notification_send == 1


def mark_notification_sent(shop_id, current_month):
    """Mark a notification as sent for the current month."""
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute(
        """
            UPDATE t_budgets SET a_notification_sent = 1
            WHERE a_shop_id = %s AND a_month = %s
        """,
        (shop_id, current_month),
    )

    conn.commit()
    cursor.close()


def set_shop_offline(shop_id):
    """set_shop_offline function sets the status of a shop to offline by setting a_online value to 0"""
    # connect to database
    conn = connect_to_db()
    cursor = conn.cursor()

    # create SQL query to update a_online value to 0
    cursor.execute("""UPDATE t_shops SET a_online = 0 WHERE a_id = %s""", (shop_id,))

    conn.commit()
    cursor.close()


def update_budget(shop_id, month, budget_amount):
    """update_budget function updates the budget information for a shop for a given month"""
    # connect to database
    conn = connect_to_db()
    cursor = conn.cursor()

    # create SQL query to update budget information for a shop for a given month
    cursor.execute(
        """
            UPDATE t_budgets SET a_budget_amount = {budget_amount}, a_notification_sent = 0,
            a_notification_current_threshold = 0 WHERE a_shop_id = &s AND a_month = %s
        """,
        (shop_id, month),
    )

    conn.commit()
    cursor.close()
