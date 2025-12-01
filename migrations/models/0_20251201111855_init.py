from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "is_verified" BOOL NOT NULL DEFAULT False,
    "verification_token" VARCHAR(255),
    "join_date" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "business" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "city" VARCHAR(255) NOT NULL DEFAULT 'Unspecified',
    "country" VARCHAR(255) NOT NULL DEFAULT 'Unspecified',
    "business_description" TEXT,
    "phone_number" VARCHAR(20),
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "logo" VARCHAR(200),
    "owner_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "product" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "category" VARCHAR(50) NOT NULL,
    "original_price" DECIMAL(10,2) NOT NULL,
    "sale_price" DECIMAL(10,2) NOT NULL,
    "discount_percentage" INT NOT NULL DEFAULT 0,
    "stock" INT NOT NULL DEFAULT 0,
    "image" VARCHAR(200),
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True,
    "business_id" UUID NOT NULL REFERENCES "business" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_product_name_683352" ON "product" ("name");
CREATE INDEX IF NOT EXISTS "idx_product_categor_5402db" ON "product" ("category");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztm/1P2zgYx/+VKj9xEodYBgydTie1tNx6o+0E7d20aYrcxAQfiZ3Fzko18b+f7bw7Sd"
    "dAA40uvwB9/DyN/fHb42/MD80lFnTo0SCgCENKtd96PzQMXMj/KJQd9jTgeWmJMDCwdKTz"
    "Muu1pMwHJuP2W+BQyE0WpKaPPIYI5lYcOI4wEpM7ImynpgCjbwE0GLEhu4M+L/jylZsRtu"
    "ADpPFH7964RdCxctVFlni2tBts7UnbYjEeXkpP8bilYRIncHHq7a3ZHcGJexAg60jEiDIb"
    "YugDBq1MM0QtoxbHprDG3MD8ACZVtVKDBW9B4AgY2u+3ATYFg558kvhx8odWA49JsECLMJ"
    "Nd9Ri2Km1z2IHiURfv+9cHb89+ka0klNm+LJREtEcZCBgIQyXXFKT8XUB5cQf8cpSxvwKT"
    "V7QZjDGepzHTXPBgOBDb7I5/fHN8vAHi3/1ryZF7SZCEj+pwuE+jIj0sE0BTgCZi6zoAY/"
    "/dAIwNKcF0EiYjcYGpB03Ea2g9Y/zlWeqnp1uw5F6VLGWZwpIEmPn1cKYhHdEi0XilNrJV"
    "LOCdwwdWjrcq/kmso8ldC/Xz5v8GoPPRp7mos0vpNyfL8WDS/yQRu+uo5Go2/TN2z3C/uJ"
    "oNFNwehwINHLhL6NcZxWpcS/AqA3ib1VWvXlz14trqQ9FcA7AizCEvYciFFctCLlLBaUWh"
    "R/Efja0TaQ4w5R18FDATk1VDScB8PBndzPuTj7lRPezPR6JEz43o2HpwpvRG8iW9f8bz9z"
    "3xsfd5Nh2pmUXiN/+siTqBgBGDt80AVhZFbI5Nud4NPOuJvZuPfK3efebc4SPUmmFnHc3c"
    "lvRstMhkOjaqfNqvDrFJncUv9m/porfdqrdp2Suse2TF22zUO+NkY3Z50nnVTfonBxtxPL"
    "y9Lz3XSBxFfpfEh8jGH+BaUhzzigBslp1oogPxgsLG0sidYEut6WzwwSo5M+cGBm8fbxVk"
    "4Yzs31z0hyNNYlwC834FfMuo4On5xApMRotIB1Hk5Ydr6ICKBDGi+TH8lnYBlXyITjJccs"
    "SKRa7uqhaAgS1rLZ4tnqQQKdFiMrCqpRgv49QpMZ0Ss7tjbwulGN5em9TUDzIxrSR5ug3I"
    "02qOp8Xsw0c2wsAxPB+ZJUNyCE3kAqciDSkEq+l5GH0UfctebwVlSIeji/Gkf8XH36Euof"
    "LEG4Ubakz7pICUAgc+CWc+sEPJvwtRqfkZHvRNiBnfVotMx7hCz6qIVsCKvb8hmMfPmPe2"
    "eMiv+puTdyfnb89OzrmLrEhiebcB9ng6VwclI+Z9DXaJ//+SFp9hZSOtemdJArpzbafndX"
    "pep+ftZc9uoechavBTJfpesvoNCHEgwBULYDZO6dQlD2yqH5N0e9czcjCbXeW6bDBW3wkt"
    "JoMRP7co2UxxN0neq9U7Pithnc6Xu4ryTKkve/dlb+n9VO5Thkhdxa9JrUtqqSVCV6yxVq"
    "tcQezRSVxtlrhEN9aVubIxbbx0tPu34tAFyKmDMAloI7/d61seoHRF/JJJveGCRibm5e4Z"
    "7VRx1c+3UVz182rFVZQ9qqnhd+gn96DqJYfZyBdMD+tuHK+SH4ZsTPk6je9Z97Dk1lb1aC"
    "2PbqcO0cStuH8J4mkRb3Tdg2ousFMh9kWFKJwPtnmjXX1yqPNGu52HhkZfaff56mPeaSWJ"
    "flSyMdUHqc/eJPuVknhprl+ih0er6KtmVTvRw6tze77n0NLLxRu3KVo+uVqSUzWyOYmpUQ"
    "Ni5N5OgM1cAyCYQVwiQv91M5tW/RdBEqKAXGDewC8WMtlhz0GUfd1PrBsoilbnNu/CRXf1"
    "TruyK4svGJSpcC+pIj3+B44QmLI="
)
