# models.py
from django.db import models

# Item max values
MAX_ITEM_NAME_LENGTH = 30
MAX_ITEM_IMAGE_FILE_NAME_LENGTH = 100
MAX_ITEM_NODE_LENGTH = 100
MAX_ITEM_DATASHEET_URL_LENGTH = 100
MAX_ITEM_PURCHASE_PLACE_URL_LENGTH = 100

# Storage max valus
MAX_STORAGE_NAME_LENGTH = 30

class Item (models.Model):
    item_id = models.BigAutoField("id of a item", primary_key=True) # INTEGER PRIMARY KEY AUTOINCREMENT
    item_name = models.CharField("name of the item", max_length=MAX_ITEM_NAME_LENGTH)    # TEXT
    item_image = models.CharField("path to the item image", max_length=MAX_ITEM_IMAGE_FILE_NAME_LENGTH)    # TEXT
    item_node = models.CharField("optional item nodes", max_length=MAX_ITEM_NODE_LENGTH, blank=True) # TEXT
    item_datasheet = models.CharField("url to the datasheet of the item", max_length=MAX_ITEM_DATASHEET_URL_LENGTH, blank=True)   # TEXT
    item_purchase_place = models.CharField("url to a possible item purchase place", max_length=MAX_ITEM_PURCHASE_PLACE_URL_LENGTH, blank=True) # TEXT

    def __str__(self) -> str:
        return self.item_name

class Storage (models.Model):
    storage_id = models.BigAutoField("id of a storage", primary_key=True)   # INTEGER PRIMARY KEY AUTOINCREMENT
    storage_name = models.CharField("costum storage name", max_length=MAX_STORAGE_NAME_LENGTH)   # VARCHAR(50)

    def __str__(self) -> str:
        return self.storage_name

class Bin (models.Model):
    bin_id = models.BigAutoField("id of a single bin", primary_key=True)    # INTEGER PRIMARY KEY AUTOINCREMENT
    storage_id = models.ForeignKey(Storage, on_delete=models.PROTECT, related_name="storages", db_column="storage_id")    # FOREIGN KEY (storage_id) REFERENCES Bins (storage_id)
    bin_number = models.PositiveIntegerField("bin number insight a single storage") # INTEGER
    bin_row = models.PositiveIntegerField("row number of the bin")  # INTEGER
    bin_col = models.PositiveIntegerField("collumn number of the bin")  # INTEGER
    bin_volume = models.FloatField("total usable volume of the bin")    # REAL
    bin_volume_used = models.PositiveIntegerField("bin volume used in percent") # INTEGER

    def __str__(self) -> str:
        string = "Bin number " + str(self.bin_number) + " inside " + str(self.storage_id)
        return string

class Stored_Item (models.Model):
    stored_item_id = models.BigAutoField("id of a stored item amount", primary_key=True)    # INTEGER PRIMARY KEY AUTOINCREMENT
    bin_id = models.ForeignKey(Bin, on_delete=models.PROTECT, related_name="bins", db_column="bin_id")    # FOREIGN KEY (bin_id) REFERENCES Bins (bin_id)
    item_id = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="items", db_column="item_id")  # FOREIGN KEY (item_id) REFERENCES Bins (item_id)
    stored_item_quantity = models.PositiveIntegerField("the quantity of the item that is stored")   # INTEGER

    def __str__(self) -> str:
        string = str(self.item_id) + " is stored " + str(self.stored_item_quantity) + " times in " + str(self.bin_id)
        return string