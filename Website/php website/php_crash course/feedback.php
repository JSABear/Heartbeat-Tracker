<?php include 'include/header.php'; ?>

<?php
$sql = 'Select * from feedback ORDER BY feedback_date DESC';
$result = mysqli_query($conn, $sql);
$feedback = mysqli_fetch_all($result, MYSQLI_ASSOC);
?>

  <h2>Feedback</h2>

  <?php if (empty($feedback)): ?>
    <p class="lead mt-3">There is no feedback</p>
  <?php endif; ?>

  <?php foreach ($feedback as $item): ?>
    <div class="card my-3 w-75">
     <div class="card-body text-center">
       <?php echo $item['name']; ?>
       <div class="text-secondary mt-2">By <?php echo $item[
         'body'
       ]; ?> on <?php echo $item[
        'feedback_date'
      ];  ?>
 </div>
     </div>
   </div>
  <?php endforeach; ?>
<?php include 'include/footer.php'; ?>