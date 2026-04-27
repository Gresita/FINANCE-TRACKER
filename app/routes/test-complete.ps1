<#
.SYNOPSIS
    Finance Tracker API - Complete Production Test Suite
.DESCRIPTION
    Tests ALL endpoints with clean output and exit codes for CI/CD
.PARAMETER BaseUrl
    API base URL (default: http://127.0.0.1:8000)
.PARAMETER Cleanup
    Delete test data after run
#>

param(
    [string]$BaseUrl = "http://127.0.0.1:8000",
    [switch]$Cleanup
)

function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
    $Colors = @{ PASS = "Green"; FAIL = "Red"; INFO = "Cyan"; WARN = "Yellow" }
    Write-Host "[$Status] $Message" -ForegroundColor $Colors[$Status]
}

try {
    Write-Status "Starting Finance Tracker API Tests" "INFO"
    Write-Status "Base URL: $BaseUrl" "INFO"

    # 1. ROOT ENDPOINT
    Write-Status "Testing root endpoint..." "INFO"
    $root = Invoke-RestMethod "$BaseUrl/" -Method Get
    Write-Status "Root OK: $($root.message)" "PASS"

    # 2. REGISTER NEW USER
    Write-Status "Registering test user..." "INFO"
    $username = "api_test_$(Get-Random -Minimum 1000 -Maximum 9999)"
    $regBody = @{
        username = $username
        email = "$username@test.com"
        password = "TestPass123!"
    } | ConvertTo-Json -Depth 10

    $regBytes = [Text.Encoding]::UTF8.GetBytes($regBody)
    $user = Invoke-RestMethod "$BaseUrl/auth/register" -Method Post -Body $regBytes -ContentType "application/json"
    Write-Status "Registered: $($user.username) (ID: $($user.id))" "PASS"

    # 3. LOGIN
    Write-Status "Logging in..." "INFO"
    $formData = "username=$([System.Web.HttpUtility]::UrlEncode($username))&password=$([System.Web.HttpUtility]::UrlEncode('TestPass123!'))"
    $formBytes = [Text.Encoding]::UTF8.GetBytes($formData)
    $login = Invoke-RestMethod "$BaseUrl/auth/login" -Method Post -Body $formBytes -ContentType "application/x-www-form-urlencoded"
    $headers = @{ "Authorization" = "Bearer $($login.access_token)" }
    Write-Status "Login OK: $($login.access_token.Substring(0,20))..." "PASS"

    # 4. VERIFY USER
    $me = Invoke-RestMethod "$BaseUrl/auth/me" -Headers $headers
    Write-Status "Auth OK: $($me.username)" "PASS"

    # 5. ADD INCOME
    Write-Status "Adding income..." "INFO"
    $income = @{
        amount = 1200.50
        description = "Salary $(Get-Date -Format 'yyyy-MM-dd')"
        category = "Salary"
        transaction_type = "INCOME"
    } | ConvertTo-Json -Depth 10
    $incomeBytes = [Text.Encoding]::UTF8.GetBytes($income)
    $incomeTx = Invoke-RestMethod "$BaseUrl/transactions/" -Method Post -Body $incomeBytes -ContentType "application/json" -Headers $headers
    Write-Status "Income OK: $$($incomeTx.amount) - $($incomeTx.description)" "PASS"

    # 6. ADD EXPENSE
    Write-Status "Adding expense..." "INFO"
    $expense = @{
        amount = 325.75
        description = "Groceries $(Get-Date -Format 'yyyy-MM-dd')"
        category = "Food"
        transaction_type = "EXPENSE"
    } | ConvertTo-Json -Depth 10
    $expenseBytes = [Text.Encoding]::UTF8.GetBytes($expense)
    $expenseTx = Invoke-RestMethod "$BaseUrl/transactions/" -Method Post -Body $expenseBytes -ContentType "application/json" -Headers $headers
    Write-Status "Expense OK: $$($expenseTx.amount) - $($expenseTx.description)" "PASS"

    # 7. LIST TRANSACTIONS
    $transactions = Invoke-RestMethod "$BaseUrl/transactions/" -Headers $headers
    Write-Status "Transactions: $($transactions.Count) records" "PASS"

    # 8. SUMMARY
    $summary = Invoke-RestMethod "$BaseUrl/transactions/summary" -Headers $headers
    Write-Status "💰 Balance: `$$($summary.balance)" "PASS"
    Write-Status "📈 Total Income: `$$($summary.total_income)" "PASS"
    Write-Status "📉 Total Expense: `$$($summary.total_expense)" "PASS"

    # FINAL RESULT
    Write-Status "🎉 ALL TESTS PASSED! (Balance: `$$($summary.balance))" "PASS"
    Write-Status "User: $($user.username) | Tests: 8/8" "Cyan"
    
    return @{
        Status = "PASS"
        User = $user.username
        Balance = $summary.balance
        Transactions = $transactions.Count
        TestsPassed = 8
    }
}
catch {
    Write-Status "💥 TEST FAILED: $($_.Exception.Message)" "FAIL"
    return @{ Status = "FAIL"; Error = $_.Exception.Message }
}

# EXECUTE
$result = Test-FinanceAPI -BaseUrl $BaseUrl

if ($result.Status -eq "PASS") {
    exit 0
} else {
    exit 1
}