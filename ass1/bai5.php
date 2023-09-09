<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>bai5</title>
    <style>
        td{
            border: 1px solid;
        }
    </style>
</head>
<?php
  // giaiphuongtrinhbac2
  function giaiphuongtrinhbac2($a,$b,$c){
    if($a == 0 ){
        if($b == 0 ){
            if($c == 0){
                $nghiem = "phuong trinh vo so nghiem ";
            }else{
                $nghiem = "phuong trinh vo nghiem ";
            }
        }else{
            $nghiem= "nghiem cua phuong trinh x= ".round(-$c/$b,2);
        }
    }else{
        $delta = pow($b,2)- 4*$a*$c;
        if($delta < 0 ){
            $nghiem= "phuong trinh vo ngiem ";
        }else if($delta == 0){
            $nghiem= "phuong trinh cos nghiem kep x1 = x2 =".-($b/2*$a);
        }else{
            $x1 = (-$b - sqrt($delta))/(2*$a);
            $x2 = (-$b + sqrt($delta))/(2*$a);
            $nghiem = "phuong trinh co 2 nghiem phan biet x1=".round($x1,2)." , x2= ".round($x2,2);
        }
    }
    return $nghiem;
  }

  if (isset($_POST["a"]) && isset($_POST["b"]) && isset($_POST["c"])){
     $nghiem=giaiphuongtrinhbac2($_POST["a"],$_POST["b"],$_POST["c"]);
}


?>
<form action="bai5.php" method="post">
<table width="744" border="1">
        <tr>
            <td style="color: black; font-size: 17px; font-weight: bold;" colspan="4" bgcolor="#336699">Giải phương trình bậc 2</td>
        </tr>

        <tr>
            <td colspan="1">Phương trình </td>
            <td>
                <input type="text" name="a">
                <label for=""> X^2 + &emsp;</label>
            </td> 
            <td>
                <input type="text" name="b">
                <label for=""> X +     &emsp; </label>
            </td>

            <td>
                <input type="text" name="c">
                <label for=""> = 0     &emsp; </label>
            </td>
        </tr>

        

        <tr>
            <td colspan="4 ">
                Nghiệm
                <input   type="text" name="" id="" value="<?php if(isset($nghiem)) echo $nghiem; ?>">

            </td>
        </tr>

        <tr>
            <td style="text-align: center;" colspan="4"><input type="submit" value="xuất" name="" id=""></td>
        </tr>
       </table>
    </form>
</body>
</html>