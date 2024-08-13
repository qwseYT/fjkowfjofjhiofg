from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipant

api_id = '256806'  # Замените на ваш api_id
api_hash = '3d07397f3c3b0db7f20a8d95'  # Замените на ваш api_hash
bot_token = '7206111288:AAEibUk7dYZCqJfyLFya4VBp7L3iWa6OKYQ'  # Замените на ваш bot_token

# Ссылка на канал, на который нужно подписаться
subscription_channel = 'https://t.me/qwsew'
subscription_channel_username = '@qwse_ew'  # Замените на @username канала

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage)
async def handler(event):
    if event.is_private:  # Игнорируем личные сообщения
        return
    
    user_id = event.sender_id
    channel = await client.get_entity(subscription_channel_username)

    try:
        # Проверяем, является ли пользователь участником канала
        participant = await client(GetParticipantRequest(channel, user_id))
        if not isinstance(participant.participant, ChannelParticipant):
            raise UserNotParticipantError("User is not a participant of the channel")
    except UserNotParticipantError:
        # Если пользователя нет в канале, удаляем сообщение и отправляем уведомление
        await event.delete()
        await event.respond(f"@{event.sender.username} Чтобы начать общение, вы должны подписаться на следующий канал: {subscription_channel_username}")
    except Exception as e:
        print(f"Ошибка: {e}")
        await event.respond(f"Произошла ошибка: {e}")
        return

client.run_until_disconnected()
