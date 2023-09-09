<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>

    <style>
        td{
            padding: 5px;
        }
    </style>
</head>
<body>
    
<?php
if (isset($_POST["so"]))
{
 if(is_numeric($_POST["so"]))
 {
 switch($_POST["so"])
{
 case 0:
 $chu="Không";
 break;
 case 1:
 $chu="Một";
 break;
 case 2:
 $chu="Hai";
 break;
 case 3:
 $chu="Ba";
 break;
 case 4:
 $chu="Bốn";
 break;
 case 5:
 $chu="Năm";
 break;
 case 6:
 $chu="Sáu";
 break;
 case 7:
 $chu="Bảy";
 break;
 case 8:
 $chu="Tám";
 break;
 case 9:
 $chu="Chín";
 break;
 default:
 $chu="Không hợp lệ";
 break;
}
}
}
?>
    <form action="bai3.php" method="POST">
        <table border="1">
            <tr>
                <td colspan="3">Đọc số</td>
            </tr>

            <tr>
                <td >Nhập số (0-9)</td>
                <td rowspan="2"><input type="submit" value="submit"></td> 
                <td>Bằng chữ</td>
                
            </tr>

            <tr>
            <td><input type="text" name="so" id=""></td>
            <td><input type="text" name="chu" id="" value="<?php echo $chu; ?>"></td>
             </tr>

            

        </table>
    </form>
</body>
</html>