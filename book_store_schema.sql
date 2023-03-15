CREATE TABLE members (
fname	VARCHAR(20) not null,
lname	VARCHAR(20) not null,
address	VARCHAR(50) not null,
city	VARCHAR(30) not null,
state	VARCHAR(20) not null,
zip		int not null,
phone	VARCHAR(12) null,
email	VARCHAR(40) not null,
userid	int auto_increment not null,
password VARCHAR(20),
creditcardtype	VARCHAR(10),
creditcardnumber	CHAR(16),
primary key(userid),
unique (email)
);

CREATE TABLE orders (
userid int not null,
ono int auto_increment,
received date not null,
shipped date,
shipAddress VARCHAR(50),
shipCity	VARCHAR(30),
shipState	VARCHAR(20),
shipZip		int,
primary key(ono),
foreign key(userid) references  members(userid)
);

CREATE TABLE books(
isbn 	CHAR(10) not null,
author	VARCHAR(100) not null,
title	VARCHAR(128) not null,
price	float not null,
subject	varchar(30) not null,
primary key(isbn)
);

CREATE TABLE odetails(
ono 	int auto_increment,
isbn	char(10),
qty 	int not null,
price	float not null,
primary key(ono, isbn),
foreign key (ono) references orders(ono),
foreign key (isbn) references books(isbn)
);

CREATE TABLE cart(
userid 	int not null,
isbn	CHAR(10) not null,
qty		int not null,
primary key (userid, isbn),
foreign key (userid) references members(userid),
foreign key (isbn) references books(isbn)
);