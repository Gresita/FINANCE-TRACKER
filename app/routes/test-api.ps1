#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Finance Tracker API - Complete Test Suite
.DESCRIPTION
    Tests ALL endpoints: register, login, transactions, summary
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$BaseUrl = "http://127.0.0.1:8000",
    
    [Parameter(Mandatory=$false)]
    [switch]$Clean = $false
)

function Write-ColorOutput {
    param([string]$Text, [string]$Color = "White")
    $Colors = @{ Green="Green"; Yellow="Yellow"; Cyan="Cyan"; Magenta="Magenta"; Red="Red"; White="White" }
    Write-Host $Text -ForegroundColor $Colors[$Color]
}

function Test-Root {
    Write-ColorOutput "🌐 ROOT TEST" "Cyan"
    $root = Invoke-RestMethod "$BaseUrl/" -Method Get
    Write-ColorOutput "✅ $($root.message)" "Green"
}

function Test-RegisterLogin {
    Write-ColorOutput "`n👤 AUTH TEST" "Yellow"
    $username = "test_$(Get-Random -Minimum 1000 -Maximum 9999)"
    $regBody = @{ 
        username = $username
        email = "$username@test.com" 
        password = "TestPass123!"
    } | ConvertTo-Json -Depth 10
    
    $regBytes = [Text.Encoding]::UTF8.GetBytes($regBody)
    $user = Invoke-RestMethod "$BaseUrl/auth/register" -Method Post -Body $regBytes -ContentType "application/json"
    
    # LOGIN (JSON)
    $loginBody = @{ username=$username; password="TestPass123!" } | ConvertTo-Json -Depth 10
    $loginBytes = [Text.Encoding]::UTF8.GetBytes($loginBody)
    $login = Invoke-RestMethod "$BaseUrl/auth/login" -Method Post -Body $loginBytes -ContentType "application/json"
    
    $script:headers = @{ "Authorization" = "Bearer $($login.access_token)" }
    $me = Invoke-RestMethod "$BaseUrl/auth/me" -Headers $headers
    
    Write-ColorOutput "✅ REGISTER: $username" "Green"
    Write-ColorOutput "✅ LOGIN: Token OK" "Green"
    Write-ColorOutput "✅ ME: $($me.username)" "Green"
    return $username
}

function Test-Transactions {
    Write-ColorOutput "`n💸 TRANSACTIONS TEST" "Yellow"
    
    # INCOME
    $income = @{ 
        amount = 1500.0
        description = "Salary $(Get-Date -Format 'yyyy-MM-dd')"
        category = "Salary"
        transaction_type = "INCOME"
    } | ConvertTo-Json -Depth 10
    $incomeBytes = [Text.Encoding]::UTF8.GetBytes($income)
    Invoke-RestMethod "$BaseUrl/transactions/" -Method Post -Body $incomeBytes -ContentType "application/json" -Headers $headers | Out-Null
    
    # EXPENSE
    $expense = @{ 
        amount = 450.75
        description = "Groceries $(Get-Date -Format 'yyyy-MM-dd')"
        category = "Food" 
        transaction_type = "EXPENSE"
    } | ConvertTo-Json -Depth 10
    $expenseBytes = [Text.Encoding]::UTF8.GetBytes($expense)
    Invoke-RestMethod "$BaseUrl/transactions/" -Method Post -Body $expenseBytes -ContentType "application/json" -Headers $headers | Out-Null
    
    Write-ColorOutput "✅ Added Income + Expense" "Green"
}

function Test-Summary {
    Write-ColorOutput "`n📊 SUMMARY TEST" "Cyan"
    $txs = Invoke-RestMethod "$BaseUrl/transactions/" -Headers $headers
    $summary = Invoke-RestMethod "$BaseUrl/transactions/summary" -Headers $headers
    
    Write-ColorOutput "📈 Transactions: $($txs.Count)" "White"
    Write-ColorOutput "💰 Balance: `$$($summary.balance)" "Green"
    Write-ColorOutput "📈 Income: `$$($summary.total_income)" "Green"
    Write-ColorOutput "📉 Expenses: `$$($summary.total_expense)" "Yellow"
    
    return $summary.balance
}

function Test-Cleanup {
    if ($Clean) {
        Write-ColorOutput "`n🧹 CLEANUP MODE" "Yellow"
        # Delete test transactions if needed
    }
}

# 🚀 MAIN TEST RUNNER
Write-ColorOutput "🧪 FINANCE TRACKER API TEST SUITE v1.0" "Magenta"
Write-ColorOutput "🌍 Base URL: $BaseUrl" "Cyan"

try {
    Test-Root
    Test-RegisterLogin
    Test-Transactions
    $balance = Test-Summary
    
    if ($balance -gt 0) {
        Write-ColorOutput "`n🎉 ALL TESTS PASSED! 💯" "Green"
        Write-ColorOutput "✅ Root, Auth, Transactions, Summary OK" "Green"
        exit 0
    } else {
        Write-ColorOutput "`n❌ BALANCE ISSUE!" "Red"
        exit 1
    }
}
catch {
    Write-ColorOutput "`n💥 TEST FAILED: $($_.Exception.Message)" "Red"
    exit 1
}
finally {
    Test-Cleanup
}