ALTER TABLE t_budgets
ADD COLUMN a_notification_sent BOOLEAN NOT NULL DEFAULT FALSE;
ADD COLUMN a_notification_current_threshold DECIMAL(10,2) DEFAULT 0;

INSERT INTO t_shops
(a_id, a_name, a_online)
VALUES
(9, 'Super Mart', 1),
(10, 'Trendy Treasures', 0),
(11, 'Fashion Fix', 1),
(12, 'Chic Choice', 0),
(13, 'Stylish Street', 1),
(14, 'Fashion Forward', 0),
(15, 'Fashion Frenzy', 1),
(16, 'Trendy Trends', 1);

INSERT INTO t_budgets
(a_shop_id, a_month, a_budget_amount, a_amount_spent)
VALUES
(9, '2023-02-01', 1150.00, 1000.67),
(10, '2023-02-01', 1050.00, 900.64),
(11, '2023-02-01', 1250.00, 1180.81),
(12, '2023-02-01', 1050.00, 954.93),
(13, '2023-02-01', 1250.00, 1105.12),
(14, '2023-02-01', 1150.00, 1155.00),
(15, '2023-02-01', 1150.00, 1150.00),
(16, '2023-02-01', 1150.00, 1004.25);