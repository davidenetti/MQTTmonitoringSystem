CREATE TABLE `hostSeen` (
	`MacAddress` VARCHAR(17) NOT NULL,
	
	PRIMARY KEY (`MacAddress`)
)

CREATE TABLE `hostInformation` (
	`IPaddress` VARCHAR(15) NOT NULL,
	`HostName` TEXT,
  	`TimeStampReceived` VARCHAR(19) NOT NULL,
  	`TimeStampStored` VARCHAR(19) NOT NULL,
  	`Propagation` TEXT,
	`MacAddress` VARCHAR(17) NOT NULL,

	PRIMARY KEY (`MacAddress`, `timeStampReceived`, `timeStampStored`)
)