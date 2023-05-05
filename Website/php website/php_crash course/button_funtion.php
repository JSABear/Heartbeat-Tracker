<?php include 'include/header.php'; ?>

<?php
if (isset($_POST['submit'])) {
  $id = $_POST['submit'];
  $name = $_POST['name'];
  $sql = "UPDATE patient_data SET patient_name='$name' WHERE patient_ID='$id'";
  if (mysqli_query($conn, $sql)) {
    header('Location: patient_state.php');
  } else {
    echo "Error updating record: " . mysqli_error($conn);
  }
}
?>

<?php include 'include/footer.php'; ?>

