DROP TABLE IF EXISTS "article";
CREATE TABLE "article" ("id" INTEGER PRIMARY KEY  NOT NULL , "title" CHAR NOT NULL  UNIQUE , "create_date" DATETIME NOT NULL , "last_update" DATETIME NOT NULL , "posted" BOOL NOT NULL  DEFAULT 0, "cate_name" VARCHAR NOT NULL , "permalink" CHAR NOT NULL, "brief" TEXT);
