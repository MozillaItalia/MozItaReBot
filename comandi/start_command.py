def start(update: Update, context: CallbackContext):

    user = update.message.from_user
    text = str(frasi["start"])

    buttons = [[InlineKeyboardButton(str(frasi["button_start"]), callback_data='1')], [InlineKeyboardButton(str(frasi["button_start2"]), callback_data='2')]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_markdown(text)
    update.message.reply_text(str(frasi["start2"]), reply_markup=reply_markup)
