# permissions for logging, metrics and alarms 

resource "aws_iam_policy" "cloudwatch_policy" {
    name = "CloudWatchPolicy"
    description = "Policy for CloudWatch logging, metrics and alarms"
    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Action = [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "logs:DescribeLogGroups",
                    "logs:DescribeLogStreams",
                    "logs:GetLogEvents",
                    "logs:FilterLogEvents"
                ],
                "Resource": "*" 
            },
            {
                Effect = "Allow"
                Action = [
                    "cloudwatch:PutMetricData",
                    "cloudwatch:GetMetricStatistics",
                    "cloudwatch:ListMetrics",
                    "cloudwatch:ListMetricStreams",
                    "cloudwatch:StartMetricStreams",
                    "cloudwatch:StopMetricStreams",
                    "cloudwatch:SetAlarmState",
                    "cloudwatch:PutMetricAlarm",
                    "cloudwatch:DescribeAlarms",
                    "cloudwatch:EnableAlarmActions",
                    "cloudwatch:DisableAlarmActions",
                    "cloudwatch:DeleteAlarms"
                ],
                "Resource": "*"
            },
            {
                Effect = "Allow"
                Action = [
                    "sns:Subscribe",
                    "sns:Publish"
                ],
                "Resource": "*"
            }
        ]
    }) 
}
resource "aws_iam_role_policy_attachment" "cloudwatch_policy" {
  role          = aws_iam_policy.cloudwatch_policy.name
  policy_arn    =  aws_iam_policy.cloudwatch_policy.arn
}



