Get-ChildItem -Directory . | ForEach-Object {
    wsl convert ./$($_.BaseName)/*.png ./$($_.BaseName)/favicon.ico
}

# wsl convert ./Small/*.png ./Small/favicon.ico
