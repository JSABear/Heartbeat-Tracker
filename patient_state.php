<?php include 'include/header.php'; ?>
<?php
$sql = 'SELECT * FROM patient_data';
$result = mysqli_query($conn, $sql);
?>

<div class="container-fluid">
  <table class="table table-bordered">
    <thead class="table-light">
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>BPM</th> 
        <th>SNS</th>
        <th>PNS</th>
        <th>Date</th>
      </tr>
    </thead>
    <tbody>
      <?php while($row = mysqli_fetch_assoc($result)) { ?>
      <tr>
        <td><?php echo $row['patient_ID']; ?></td>
        <td>
          <form action="button_funtion.php" method="POST">
            <input type="text" name="name" value="<?php echo $row['patient_name']; ?>" />
            <input type="hidden" name="id" value="<?php echo $row['patient_ID']; ?>" />
            <button type="submit" name="submit" value="<?php echo $row['patient_ID']; ?>" class="btn btn-outline-secondary">Save</button>
          </form>
        </td> 
        <td><?php echo $row['BPM']; ?></td>
        <td><?php echo $row['PNS']; ?></td>
        <td><?php echo $row['SNS']; ?></td>
        <td><?php echo $row['created_at']; ?></td>
      </tr>
      <?php } ?>
    </tbody>
  </table>
</div>

<?php include 'include/footer.php'; ?>
