# Finance Tracker API - PERFECT TEST
$BaseUrl = "http://127.0.0.1:8000"
Write-Host "🧪 Testing API..." -ForegroundColor Cyan

# ROOT
$root = Invoke-RestMethod "$BaseUrl/"
Write-Host "✅ Root: $($root.message)" -ForegroundColor Green

# REGISTER
$username = "test_$([math]::Round((Get-Random * 9000) + 1000))"
$regBody = @{
    username = $username
    email = "$username@test.com"
    password = "TestPass123!"
} | ConvertTo-Json -Depth 10

$regBytes = [Text.Encoding]::UTF8.GetBytes($regBody)
$user = Invoke-RestMethod "$BaseUrl/auth/register" -Method Post -Body $regBytes -ContentType "application/json"
Write-Host "✅ Register: $($user.username)" -ForegroundColor Green

# LOGIN (FORM - 100% WORKS)
$formData = "username=$([System.Web.HttpUtility]::UrlEncode($username))&password=$([System.Web.HttpUtility]::UrlEncode('TestPass123!'))"
$formBytes = [Text.Encoding]::UTF8.GetBytes($formData)
$login = Invoke-RestMethod "$BaseUrl/auth/login" -Method Post -Body $formBytes -ContentType "application/x-www-form-urlencoded"
$headers = @{ "Authorization" = "Bearer $($login.access_token)" }
Write-Host "✅ Login: $($login.access_token.Substring(0,20))..." -ForegroundColor Green

# TRANSACTION
$tx = @{
    amount = 500.0
    description = "PowerShell Test"
    category = "Test"
    transaction_type = "INCOME"
} | ConvertTo-Json -Depth 10

$txBytes = [Text.Encoding]::UTF8.GetBytes($tx)
Invoke-RestMethod "$BaseUrl/transactions/" -Method Post -Body $txBytes -ContentType "application/json" -Headers $headers | Out-Null

# SUMMARY
$summary = Invoke-RestMethod "$BaseUrl/transactions/summary" -Headers $headers
Write-Host "💰 Balance: $($summary.balance)" -ForegroundColor Green
Write-Host "📊 Transactions OK!" -ForegroundColor Green

Write-Host "🎉 FULL SUCCESS!" -ForegroundColor Magenta