<?php
if (isset($_POST["ten"]))
{
$ten=$_POST["ten"];
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
 <style>
    body{
        display: flex;
    }
    tr td{
        border: 2px solid;
    }

    td{
        padding : 5px;
    }

    #td1{
        background-color: blueviolet;
        color: black;
        text-align: center;
        font-weight: bold;
        font-size: 30px;
    }
 </style>
<body>

<form action="bai1.php" method="post">
    
   <table>
    <tr>
        <td  id="td1"  colspan="2" >In lời chào</td>
    </tr>
    
    <tr>
        <td >Họ tên bạn</td>
        <td>
            <input type="text" name="ten" id="">
        </td>
    </tr>

    <tr>
        <td  colspan="2"><label value=""></label> <?php echo " Chào bạn ".$ten; ?>
        </label></td>

    </tr>

    <tr>
        <td style="text-align: center ;" colspan="2"><input type="submit" value="xuất"></td>
    </tr>

    
   </table>
</form>
</body>
</html>