<?php
# Meeuwenstraat Energy Monitor Target

/** The name of the database for WordPress */
define('DB_NAME', 'ur_dbname');

/** MySQL database username */
define('DB_USER', 'ur_dbuser');

/** MySQL database password */
define('DB_PASSWORD', 'ur_pwd');

/** MySQL hostname */
define('DB_HOST', 'localhost');


$db = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
$post = $_POST;

if( isset ( $post['state'] )){
	$states = json_decode($post['state'], true);
	foreach($states as $state){
		$db->query(sprintf('INSERT INTO `energy` SET `time` = %d, `energy_t1` = %.02f, `energy_t2` = %.02f, `gas` = %.02f, `power` = %.03f', $state['time'] , $state['energy_t1'], $state['energy_t2'] , $state['gas'], $state['power']));
	}
	echo 'OK';
} else {
	echo 'No state sent';
}

$db->close();

