CREATE TABLE "Ingridient" (
	"id" serial NOT NULL,
	"name" char(256) NOT NULL,
	"price" money NOT NULL,
	"description" TEXT NOT NULL,
	CONSTRAINT "Ingridient_pk" PRIMARY KEY ("id")
);

CREATE TABLE "Restaurants" (
	"id" serial NOT NULL,
	"name" char(256) NOT NULL UNIQUE,
	"description" TEXT NOT NULL,
	CONSTRAINT "Restaurants_pk" PRIMARY KEY ("id")
);

CREATE TABLE "Dish_types" (
	"id" serial NOT NULL,
	"name" char(256) NOT NULL UNIQUE,
	"description" TEXT NOT NULL,
	CONSTRAINT "Dish_types_pk" PRIMARY KEY ("id")
);

CREATE TABLE "Dishes" (
	"id" serial NOT NULL,
	"dish_name" char(256) NOT NULL,
	"dish_cost" money NOT NULL,
	"dish_description" TEXT,
	"dish_type_id" integer NOT NULL,
	"restaraun_id" bigint NOT NULL,
	CONSTRAINT "Dishes_pk" PRIMARY KEY ("id"),
    FOREIGN KEY ("dish_type_id") REFERENCES "Dish_types"("id"),
    FOREIGN KEY ("restaraun_id") REFERENCES "Restaurants"("id")
);



CREATE TABLE "Customer" (
	"name" char(256) NOT NULL,
	"id" serial NOT NULL,
	"surname" char(256) NOT NULL,
	"balance" money NOT NULL,
	"date_born" DATE NOT NULL,
	"sex" bool NOT NULL,
	"username" char(128) NOT NULL UNIQUE,
	CONSTRAINT "Customer_pk" PRIMARY KEY ("id")
);



CREATE TABLE "Purchase" (
	"customer_id" bigint NOT NULL,
	"time_bought" TIMESTAMP,
	"id" serial NOT NULL,
	"complete" bool NOT NULL,
	"current_price" money DEFAULT 0,
	CONSTRAINT "Purchase_pk" PRIMARY KEY ("id"),
	FOREIGN KEY ("customer_id") REFERENCES "Customer"("id")
);


CREATE TABLE "Menu2Ingridient" (
	"id" serial NOT NULL,
	"ingridient_id" bigint NOT NULL,
	"dish_id" bigint NOT NULL,
	CONSTRAINT "Menu2Ingridient_pk" PRIMARY KEY ("id"),
	FOREIGN KEY ("ingridient_id") REFERENCES "Ingridient"("id"),
	FOREIGN KEY ("dish_id") REFERENCES "Dishes"("id")
);


CREATE TABLE "Providers" (
	"id" serial NOT NULL,
	"name" char(256) NOT NULL UNIQUE,
	"description" TEXT NOT NULL,
	CONSTRAINT "providers_pk" PRIMARY KEY ("id")
);



CREATE TABLE "Ingridient2Provider" (
	"id" serial NOT NULL,
	"ingridient_id" bigint NOT NULL,
	"provider_id" bigint NOT NULL,
	"time_to_deliver" DATE NOT NULL,
	CONSTRAINT "Ingridient2Provider_pk" PRIMARY KEY ("id"),
	FOREIGN KEY ("ingridient_id") REFERENCES "Ingridient"("id"),
	FOREIGN KEY ("provider_id") REFERENCES "Providers"("id")
);



CREATE TABLE "Purchase2Dishes" (
	"id" serial NOT NULL,
	"purchase_id" bigint NOT NULL,
	"dishes_id" bigint NOT NULL,
	CONSTRAINT "Purchase2Dishes_pk" PRIMARY KEY ("id"),
	FOREIGN KEY ("purchase_id") REFERENCES "Purchase"("id"),
	FOREIGN KEY ("dishes_id") REFERENCES "Dishes"("id")
);