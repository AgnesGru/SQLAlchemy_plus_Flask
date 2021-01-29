import sqlite3  # biblioteka do obsługi prostego silnika

conection = sqlite3.connect('sklep.db')  # tworzy bazę
cursor = conection.cursor()
# cursor służy do uruchomiania zapytań SQL, zwraca też dane z zapytań

# tworzenie tabel

# create_tabel = "Create Table If Not Exists Customer (Id int, Name text, Surname text)"
# cursor.execute(create_tabel)

# zmienianie tabel

# alter_table = 'Alter Table Customer Add Column Gender text'
# cursor.execute(alter_table)

# drop table

# alter_table = 'Drop Table Customer'
# cursor.execute(alter_table)

# create_table = 'Create Table If Not Exists City(Id int Primary Key, Name text, Population int)'
# cursor.execute(create_table)
# create_table = "Create Table If Not Exists Product(Id int Primary Key, Name text, Price real)"
# cursor.execute(create_table)
# create_table = 'Create Table If Not Exists Customer(Id int Primary Key, Name text, Gender text Check(Gender = "M" or ' \
#                'Gender = "F"), CityId int, Foreign Key(CityId) References City(Id))'
# cursor.execute(create_table)
# create_table = 'Create Table If Not Exists [Order](Id int Primary Key, OrderDate text, CustomerId int, ProductId int, ' \
#                'Foreign Key(CustomerId) References Customer(Id), Foreign Key(ProductId) References Product(Id)) '
# cursor.execute(create_table)

# alter examples

# alter_table = 'Alter Table Customer Add Column Email text'
# cursor.execute(alter_table)
# alter_table = 'Alter Table Customer Alter Column Email text' #????
# cursor.execute(alter_table)
# alter_table = 'Alter Table Customer Add Column AccountId int Not Null Default(0)'
# cursor.execute(alter_table)
# alter_table = 'Alter Table Customer Drop Column Email'
# cursor.execute(alter_tabel)

# get or change data: select, insert, update, delete
# miasto = (1, 'Cieplewo', 2000)
# insert_city = 'Insert into City (Id, Name, Population) Values (?, ?, ?)'
# cursor.execute(insert_city, miasto)
# conection.commit()
# conection.close()

# instert_cities = 'Insert into City (Id, Name, Population) Values (?, ?, ?)'
# miasta = [(3, 'Sopot', '40000'),
#           (4, "Katowice", '600000'),
#           (5, 'Zalesie', '100'),
#           (6, 'Zalesie', '200')]
# cursor.executemany(instert_cities, miasta)
# conection.commit()
# conection.close()

# Update

# update_city = "Update City Set Population = ?  where Name = ?"
# cursor.execute(update_city, ('300000', 'Katowice'))
# conection.commit()

# Delete
delete_city = 'Delete from City where Name = ?'
cursor.execute(delete_city, ('Katowice',))
conection.commit()
conection.close()