from cards import CardType
import cards as Cards_File
from Player import print_cards_player

#наверно в DiceManager лучше не вести учет количества карт у игрока, так как это и такк ведется в классе игрока. вместо этого лучше ссылаться на объект игрока и с ним работать
class DiceManager:
    listeners = [{}, {}, {}, {}] #listeners: [{dice number: {player id: {card id : number of cards}}}]

    def subscribe(self, dice_list, card, player: int, color: CardType):
        for dice in dice_list:
            listeners_item = self.listeners[color.value].get(dice)
            
            if not listeners_item:
                self.listeners[color.value][dice] = {player : {card.id : 1}}
            else:
                player_cards = listeners_item.get(player)

                if not player_cards:
                    listeners_item[player] = {card.id : 1}
                else:
                    card_num = player_cards.get(card.id)
                    if card_num:
                        player_cards[card.id] += 1
                    else:
                        player_cards[card.id] = 1

    def unsubscribe(self, dice_list, card, player: int, color: CardType):
        for dice in dice_list:
            listeners_item = self.listeners[color.value].get(dice)
            
            if listeners_item:
                player_cards = listeners_item.get(player)

                if player_cards:
                    card_id = player_cards.get(card.id)
                    if card_id:
                        del player_cards[card.id]

    def process_dice_red(self, dice, active_player, players: list):
        reds = self.listeners[CardType.RED.value].get(dice)
        if not reds:
            return
        
        reds_list = list(reds.items())
        reds_list.reverse()
        for player_id, cards in reds_list:
            if player_id == active_player.id:
                continue

            card_id, number = list(cards.items())[0]
            card_profit = Cards_File.red_cards[card_id].profit

            #проверяем наличие карты Торговый центр
            if players[player_id].cards[CardType.WIN.value].get(1) != None and \
                    card_id in Cards_File.win_cards[1].depends[CardType.RED.value]:
                card_profit += 1

            need_to_pay = number * card_profit

            if active_player.money == 0:
                break
            elif active_player.money < need_to_pay:
                players[player_id].money += active_player.money
                active_player.money = 0
                print("\nred pay player {} now have {} money".format(active_player.id, active_player.money))
                print("\nred pay player {} now have {} money".format(player_id, players[player_id].money))
                break
            else:
                players[player_id].money += need_to_pay
                active_player.money -= need_to_pay
                print("\nred pay player {} now have {} money".format(active_player.id, active_player.money))
                print("\nred pay player {} now have {} money".format(player_id, players[player_id].money))

    def process_dice_blue(self, dice, players: list):
        blues = self.listeners[CardType.BLUE.value].get(dice)
        if not blues:
            return
        
        for player_id, cards in blues.items():
            card_id, number = list(cards.items())[0]
            need_to_pay = number * Cards_File.blue_cards[card_id].profit
            players[player_id].money += need_to_pay
            print("\nblue pay player {} now have {} money".format(player_id, players[player_id].money))

    def process_dice_green(self, dice, active_player_id, players: list):
        greens = self.listeners[CardType.GREEN.value].get(dice)
        if not greens:
            return
        
        green_cards = greens.get(active_player_id)
        if not green_cards:
            return

        green_card_id, green_card_number = list(green_cards.items())[0]
        card_profit = Cards_File.green_cards[green_card_id].profit

        #проверяем наличие карты Торговый центр
        if players[active_player_id].cards[CardType.WIN.value].get(1) != None and \
                green_card_id in Cards_File.win_cards[1].depends[CardType.GREEN.value]:
            card_profit += 1

        if Cards_File.green_cards[green_card_id].depends == []:
            need_to_pay = card_profit
        else:
            need_to_pay = 0
            for blue_card_id in Cards_File.green_cards[green_card_id].depends:
                blue_card_number = players[active_player_id].cards[CardType.BLUE.value].get(blue_card_id)

                if blue_card_number != None:
                    need_to_pay += blue_card_number * card_profit
        
        need_to_pay *= green_card_number
        players[active_player_id].money += need_to_pay
        print("\ngreen pay player {} now have {} money".format(active_player_id, players[active_player_id].money))

    def process_dice_purple(self, dice, active_player_id, players: list):
        purples = self.listeners[CardType.PURPLE.value].get(dice)
        if not purples:
            return
        
        purple_cards = purples.get(active_player_id)
        if not purple_cards:
            return
        
        for card_id, _ in purple_cards.items():
            if card_id == 0: #взять деньги у всех
                need_to_pay = Cards_File.purple_cards[card_id].profit
                for player in players:
                    if player.id == active_player_id:
                        continue
                    if player.money == 0:
                        continue
                    elif player.money < need_to_pay:
                        players[active_player_id].money += player.money
                        player.money = 0
                        print("\npay player {} now have {} money".format(active_player_id, players[active_player_id].money))
                        print("\npay player {} now have {} money".format(player.id, player.money))
                    else:
                        players[active_player_id].money += need_to_pay
                        player.money -= need_to_pay
                        print("\npay player {} now have {} money".format(active_player_id, players[active_player_id].money))
                        print("\npay player {} now have {} money".format(player.id, player.money))
            
            elif card_id == 1:#обмен картами
                while True:
                    ans = self.exchange_cards_by_purple(players, active_player_id)
                    if ans:
                        break
            else:#взять у одного игрока 5 монет
                self.get_5_monets_from_any_player(players, active_player_id)
    
    def get_5_monets_from_any_player(self, players, active_player_id, card_id=2):
        while True:
            print("Игроки: ")
            for player in players:
                if player.id == active_player_id:
                    continue
                self.print_player_cards(player)
            ans = input("Введите id другого игрока или 'n' для отмены: ")
            if ans == 'n':
                return
            
            need_to_pay = Cards_File.purple_cards[card_id].profit
            other_player_id = int(ans)
            if other_player_id == active_player_id:
                print('Вы ввели свой id, попробуйте заново')
                continue
            if players[other_player_id].money == 0:
                break
            elif players[other_player_id].money < need_to_pay:
                players[active_player_id].money += players[other_player_id].money
                players[other_player_id].money = 0
                print("\npay player {} now have {} money".format(active_player_id, players[active_player_id].money))
                print("\npay player {} now have {} money".format(other_player_id, players[other_player_id].money))
                break
            else:
                players[active_player_id].money += need_to_pay
                players[other_player_id].money -= need_to_pay
                print("\npay player {} now have {} money".format(active_player_id, players[active_player_id].money))
                print("\npay player {} now have {} money".format(other_player_id, players[other_player_id].money))
                break

    def exchange_cards_by_purple(self, players, active_player_id):
        print("Игроки: ")
        for player in players:
            if player.id == active_player_id:
                continue
            print_cards_player(player)

        ans = input("Введите id другого игрока или 'n' для отмены: ")
        if ans == 'n':
            return True
        
        other_player_id = int(ans)
        if active_player_id == other_player_id:
            print("Вы ввели свой id, попробуйте снова")
            return False

        other_player_input_color = int(input("\nВведите цвет карты другого игрока (RED = 0, BLUE = 1, GREEN = 2, PURPLE = 3): "))
        other_player_card_id = int(input("Введите id карты другого игрока: "))

        active_player_input_color = int(input("\nВведите цвет своей карты (RED = 0, BLUE = 1, GREEN = 2, PURPLE = 3): "))
        active_player_card_id = int(input("Введите id своей карты: "))

        players[other_player_id].del_card(other_player_card_id, CardType(other_player_input_color), self.unsubscribe)
        players[other_player_id].add_card(active_player_card_id, CardType(active_player_input_color), self.subscribe)

        players[active_player_id].del_card(active_player_card_id, CardType(active_player_input_color), self.unsubscribe)
        players[active_player_id].add_card(other_player_card_id, CardType(other_player_input_color), self.subscribe)
        return True