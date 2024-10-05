from player.player import Player

# Create a player and show their initial stats and quests.
player = Player("Hero")
player.display_stats()
player.show_all_quests()

# Adding and showing custom quests
print("\nAdding a custom quest 'Learn Python for 30 minutes'...")
player.add_custom_quest("Learn Python for 30 minutes", "Enhance coding skills.", 100)
player.show_all_quests()

# Complete a quest and show stats.
print("\nCompleting 'Read a book for 10 minutes' quest...")
player.complete_quest("Read a book for 10 minutes")
player.display_stats()