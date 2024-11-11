# models.py
from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404

# Item max values
MAX_ITEM_NAME_LENGTH = 30
MAX_ITEM_IMAGE_FILE_NAME_LENGTH = 100
MAX_ITEM_NODE_LENGTH = 255
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
    storage_number_of_rows = models.IntegerField("number of storage rows")

    def __str__(self) -> str:
        return self.storage_name
    
    def all_bins_sorted_in_rows(self) -> dict:
        all_bins_per_row = dict()
        for row_number in range(self.storage_number_of_rows):
            all_bins_per_row[row_number] = Bin.objects.filter(storage_id = self.storage_id, bin_row = row_number)
        return all_bins_per_row

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
    stored_item_storedate = models.DateTimeField("the last date of storage at this location", auto_now_add=True)    # TEXT

    def __str__(self) -> str:
        string = str(self.item_id) + " is stored " + str(self.stored_item_quantity) + " times in " + str(self.bin_id)
        return string
    
    @classmethod    # This decorator defines that this method is used without a instance if the class
    def get_total_stored_quantity_of_one_item(cls, item_id) -> int:  # cls needs to be used in a class method like self
        """Summes up the total quantity of one item

        Args:
            cls: Stored_Item class object
            item_id: Primmary key of the item

        Returns:
            The summed up quantity of the item
        """
        return cls.objects.filter(item_id=item_id).aggregate(total_quantity=Sum('stored_item_quantity'))['total_quantity'] or 0
    
    @classmethod
    def get_total_stored_quantity_for_all_items(cls) -> models.QuerySet:
        """Summes up the total quantity per stored item

        Args:
            cls: Stored_Item class object

        Returns:
            total_stored_quantity_all_items: A list with the item dataset and the total quantity that is stored of the item
        """
        # List to return
        total_stored_quantity_all_items = list()
        # Groups all same items and sums the quantitys of them
        total_stored_quantity_per_item = cls.objects.values('item_id').annotate(total_quantity=Sum('stored_item_quantity'))

        # Build the list to return the summed up quantitys and items
        for item in total_stored_quantity_per_item:
            total_stored_quantity_all_items.append((get_object_or_404(Item, pk=item['item_id']), item['total_quantity']))

        return total_stored_quantity_all_items
    
    @classmethod
    def get_stored_item_last_in_first_out_list(cls, item_id) -> list:
        """ Builds a list which is orderd from latest storage date to earlyest storage date

        This Method is a class method which does not require a instance of the class

        Returns:
            A list list which is orderd from latest storage date to earlyest storage date
        """
        return cls.objects.filter(item_id=item_id).order_by('-stored_item_storedate')