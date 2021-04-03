create database LIVE_SCORE
go

use LIVE_SCORE
go

create table ACCOUNT
(
	USERNAME_ nvarchar(20),
	PASSWORD_ nvarchar(20),
	ROLE_ nchar(6),
	STATUS_ bit
	primary key (USERNAME_)
)
go

alter table ACCOUNT
add constraint A_ROLE
check (ROLE_ in ('Admin','Client'))
go

insert ACCOUNT
values ('admin','admin','Admin',0)
go