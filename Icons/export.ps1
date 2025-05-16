mkdir -Force ./Regular, ./Small, ./Small_Outlined, ./Small_Inverted | Out-Null

256, 96, 80, 72, 64, 60, 48, 40, 36, 32, 30, 24, 20, 16 | ForEach-Object {
    & "C:\Program Files\Inkscape\bin\inkscape.exe" -w $_ -h $_ -o "./Regular/$_.png" './Arkanis_Icon_Regular.svg'
    & "C:\Program Files\Inkscape\bin\inkscape.exe" -w $_ -h $_ -o "./Small/$_.png" './Arkanis_Icon_Small.svg'
    & "C:\Program Files\Inkscape\bin\inkscape.exe" -w $_ -h $_ -o "./Small_Outlined/$_.png" './Arkanis_Icon_Small_Outlined.svg'
    & "C:\Program Files\Inkscape\bin\inkscape.exe" -w $_ -h $_ -o "./Small_Inverted/$_.png" './Arkanis_Icon_Small_Inverted.svg'
}
