<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>bai4</title>
    <style>
        #first{
            padding-right: 15px;
        }
    </style>
</head>
<body>

<?php
 if(isset($_POST["sodau"]) && isset($_POST["socuoi"])){
    $sodau=$_POST["sodau"];
    $socuoi=$_POST["socuoi"];
    $tong= 0;
    $tongchan= 0;
    $tongle=0;
    $tich = 1;
    for($i=$sodau; $i <= $socuoi; $i++)
        $tong = $tong + $i;
    for($i=$sodau; $i <= $socuoi; $i++)
        $tich = $tich*$i;
    for($i=$sodau; $i <= $socuoi; $i++)
       if ($i%2==0)
       $tongchan=$tongchan+$i;
    for($i=$sodau; $i <= $socuoi; $i++)
      if ($i%2!=0)
      $tongle=$tongle+$i;


        
    

 }
?>

    <form action="bai4.php" method="post">
        <table  border="1">
            <tr>
                <td id="first" >&emsp;</td>
                <td >Số bắt đầu
                    <input type="text" name="sodau"  value="<?php if(isset($_POST["sodau"])) echo $_POST["sodau"]; ?>" >
                </td>
                <td >Số kết thúc 
                    <input type="text" name="socuoi" value="<?php if(isset($_POST["socuoi"])) echo $_POST["socuoi"]; ?>">
                 </td>
            </tr>

            <tr>
                <td colspan="3">kết quả</td>
            </tr>

            <tr>
                <td  id="first">Tích các số </td>
                <td colspan="2">
                    <input type="text" name="tich"  value="<?php if(isset($tich)) echo $tich; ?>">
                </td>
            </tr>

            <tr>
                <td  id="first">Tổng các số </td>
                <td colspan="2">
                    <input type="text" name="tong" value="<?php if(isset($tong)) echo $tong; ?>">
                </td>
            </tr>

            <tr>
                <td  id="first">Tổng các số chẵn</td>
                <td colspan="2">
                    <input type="text" name="tongchan"  value="<?php if(isset($tongchan)) echo $tongchan; ?>">
                </td>
            </tr>

            <tr>
                <td  id="first">Tổng các số lẻ</td>
                <td colspan="2">
                    <input type="text" name="tongle"  value="<?php if(isset($tongle)) echo $tongle; ?>">
                </td>
            </tr>

            <tr>
                <td colspan="3">
                    <input style="margin: 2px;" type="submit" value="Tính toán">
                </td>
            </tr>
            
        </table>
    </form>
    
</body>
</html>