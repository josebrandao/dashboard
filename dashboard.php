<?php
echo "<h1> Dashboard</h1>";
	    // Inicia o cURL acessando uma URLht
	    $cURL = curl_init('https://dax-rest.comscore.com/v1/reportitems.xml?itemid=10025&startdate=20140301&enddate=20140316&nrofrows=8&site=r7-portal&format=json&client=r7&user=api&password=15l58841v');
	    // Define a opção que diz que você quer receber o resultado encontrado
	    curl_setopt($cURL, CURLOPT_RETURNTRANSFER, true);
	    // Executa a consulta, conectando-se ao site e salvando o resultado na variável $resultado
	    $resultado = curl_exec($cURL);
	    // Encerra a conexão com o site
		echo $resultado;
	    curl_close($cURL);
		// Abre ou cria o arquivo bloco1.txt
		// "a" representa que o arquivo é aberto para ser escrito
		$fp = fopen("data/10025.json", "w+");
		// Escreve "exemplo de escrita" no file .json
		$escreve = fwrite($fp, $resultado);
		// Fecha o arquivo
		fclose($fp);
		
	?>