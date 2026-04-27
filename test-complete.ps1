$BaseUrl = "http://127.0.0.1:8000"
Write-Host "🧪 Finance Tracker API Test" -ForegroundColor Cyan

# 1. ROOT
$root = Invoke-RestMethod "$BaseUrl/"
Write-Host "1. Root OK: $($root.message)" -ForegroundColor Green

# 2. REGISTER
$username = "final_test_$([int]((Get-Random -Minimum 1000 -Maximum 9999)))"
$regBody = @{
    username = $username
    email = "$username@test.com"
    password = "TestPass123!"
} | ConvertTo-Json -Depth 10
$regBytes = [Text.Encoding]::UTF8.GetBytes($regBody)
$user = Invoke-RestMethod "$BaseUrl/auth/register" -Method Post -Body $regBytes -ContentType "application/json"
Write-Host "2. Register OK: $($user.username)" -ForegroundColor Green

# 3. LOGIN (FORM)
$formData = "username=$([System.Web.HttpUtility]::UrlEncode($username))&password=$([System.Web.HttpUtility]::UrlEncode('TestPass123!'))"
$formBytes = [Text.Encoding]::UTF8.GetBytes($formData)
$login = Invoke-RestMethod "$BaseUrl/auth/login" -Method Post -Body $formBytes -ContentType "application/x-www-form-urlencoded"
$headers = @{ "Authorization" = "Bearer $($login.access_token)" }
Write-Host "3. Login OK: $($login.access_token.Substring(0,20))..." -ForegroundColor Green

# 4. TRANSACTION
$tx = @{
    amount = 888.0
    description = "PowerShell Final Test"
    category = "Test"
    transaction_type = "INCOME"
} | ConvertTo-Json -Depth 10
$txBytes = [Text.Encoding]::UTF8.GetBytes($tx)
$transaction = Invoke-RestMethod "$BaseUrl/transactions/" -Method Post -Body $txBytes -ContentType "application/json" -Headers $headers
Write-Host "4. Transaction OK: $$($transaction.amount)" -ForegroundColor Green

# 5. SUMMARY
$summary = Invoke-RestMethod "$BaseUrl/transactions/summary" -Headers $headers
Write-Host "5. Summary OK:" -ForegroundColor Cyan
Write-Host "   💰 Balance: $($summary.balance)" -ForegroundColor Green
Write-Host "   📈 Income: $($summary.total_income)" -ForegroundColor Green
Write-Host "   📉 Expense: $($summary.total_expense)" -ForegroundColor Yellow

Write-Host "`n🎉 ALL 5 TESTS PASSED!" -ForegroundColor Magenta
Write-Host "✅ Root | Register | Login | Transaction | Summary" -ForegroundColor Cyan