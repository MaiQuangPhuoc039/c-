<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>bai2</title>
    <style>
        td{
            border: 1px solid;
        }
    </style>
</head>
<?php
  if(isset($_POST["a"]) && isset($_POST["b"])){
    $a = $_POST["a"];
    $b = $_POST["b"];
    if($a == 0){
        if($b == 0)
            $nghiem = "Phuong trinh co vo so nghiem";
        if($b<>0)
            $nghiem = "Phuong trinh vo nghiem ";
        
    }else{
        $x = -($b/$a);
        $x=round($x,2);
        $nghiem= "x= $x";
    }
  }
?>
<form action="a.php" method="post">
<table width="744" border="1">
        <tr>
            <td style="color: black; background-color: blueviolet; font-size: 17px; font-weight: bold;" colspan="3">Giải phương trình bậc 1</td>
        </tr>

        <tr>
            <td colspan="1">Phương trình </td>
            <td>
                <input type="text" name="a">
                <label for=""> X + &emsp;</label>
            </td> 
            <td>
                <input type="text" name="b">
                <label for=""> = 0    &emsp; </label>
            </td>
        </tr>

        <tr>
            <td colspan="3 ">
                <label for="">Nghiệm</label>
                <input type="text" name="" id="" value="<?php if(isset($nghiem)) echo $nghiem; ?>">

            </td>
        </tr>

        <tr>
            <td style="text-align: center;" colspan="3"><input type="submit" value="xuất" name="" id=""></td>
        </tr>
       </table>
    </form>
</body>
</html>