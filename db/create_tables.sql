CREATE TABLE usuario(
  id_usuario serial NOT NULL,
  matricula varchar(15) NOT NULL,
  nome varchar(30) NOT NULL,
  cpf varchar(15) NOT NULL,
  email varchar(50) NOT NULL,
  senha varchar(15) NOT NULL,
  status varchar(10),
  PRIMARY KEY (id_usuario)
);


CREATE TABLE motorista(
  id_motorista serial NOT NULL,
  matricula varchar(15) NOT NULL,
  nome varchar(30) NOT NULL,
  cnh varchar(15) NOT NULL,
  status varchar(10),
  CONSTRAINT motorista_pkey PRIMARY KEY (id_motorista)
);

CREATE TABLE veiculo(
  id_veiculo serial NOT NULL,
  placa varchar(10) NOT NULL,
  modelo varchar(20) NOT NULL,
  status varchar(10) NOT NULL,
  PRIMARY KEY (id_veiculo)
);


CREATE TABLE revisao(
  id_revisao serial NOT NULL,
  cod_veiculo integer NOT NULL,
  descricao varchar(500) NOT NULL,
  data_revisao date NOT NULL,
  status varchar(10),
  PRIMARY KEY (id_revisao),
  FOREIGN KEY (cod_veiculo) REFERENCES veiculo (id_veiculo)
);


CREATE TABLE viagem(
  id_viagem serial NOT NULL,
  cod_veiculo integer NOT NULL,
  cod_motorista integer NOT NULL,
  data_saida date NOT NULL,
  data_chegada date,
  km_saida varchar(30) NOT NULL,
  km_chegada varchar(30),
  solicitante varchar(20) NOT NULL,
  descricao varchar(500) NOT NULL,
  status varchar(10),
  PRIMARY KEY (id_viagem),
  FOREIGN KEY (cod_motorista) REFERENCES motorista (id_motorista),
  FOREIGN KEY (cod_veiculo) REFERENCES veiculo (id_veiculo)
);
