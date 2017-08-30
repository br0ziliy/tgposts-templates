#!/bin/env python

# -*- coding: utf-8 -*-
from telegram.ext import (Updater, MessageHandler, Filters, CommandHandler,
ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging, os
import importlib
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token='')
dispatcher = updater.dispatcher

def start(bot, update):
    frm = update.message.from_user.username
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="Hi {}, I'm Lucas \
Goodwin. Nice to meet you. I'll help you to deal with your channel \
posts.".format(frm))
    templates_dir = "templates/{}".format(frm)
    if os.path.exists(templates_dir):
        templates_list = []
        for f in os.listdir(templates_dir):
            if f.endswith('.pyc') or f == '__init__.py': continue
            f = f.split('.')[0]
            templates_list.append([f])
        markup = ReplyKeyboardMarkup(templates_list, one_time_keyboard=True)
        update.message.reply_text("Select your template (or /cancel):", reply_markup=markup)
        return 'conversation_got_template'
    else:
        update.message.reply_text("I don't have any templates for \
you, please contact @br0ziliy to add some. Bye.")
        return ConversationHandler.END

def process_template(bot, update, user_data):
    frm = update.message.from_user.username
    chat_id = update.message.chat_id
    template = update.message.text
    templates_dir = "templates/{}".format(frm)
    template_fname = "templates.{}.{}".format(frm, template)
    if os.path.exists(templates_dir):
        logging.info(">>> Importing {}".format(template_fname))
        template_mod = importlib.import_module(template_fname, template_fname)
        t = template_mod.Template()
        params = t.get_params()
        user_data['params'] = params
        user_data['template'] = t
        markup = ReplyKeyboardMarkup([params.keys()], one_time_keyboard=True)
        update.message.reply_text('[process_template] Current parameters: \
{}'.format([params]), disable_web_page_preview=True)
        update.message.reply_text('Choose param to set (or /done):', reply_markup=markup)
        return 'conversation_choose_param'
    else:
        logging.error(">>> Path {} not found".format(templates_dir))
        bot.send_message(chat_id=chat_id, text="Hmm, something is not right, \
templates path not found.")
        return ConversationHandler.END

def process_params(bot, update, user_data):
    params = user_data['params']
    markup = ReplyKeyboardMarkup([params.keys()], one_time_keyboard=True)
    update.message.reply_text('[process_params] Current parameters: \
{}'.format([params]), disable_web_page_preview=True)
    update.message.reply_text('Choose param to set (or /done):', reply_markup=markup)
    return 'conversation_choose_param'

def choose_param(bot, update, user_data):
    p = update.message.text
    user_data['cur_param'] = p
    update.message.reply_text("Parameter: {}\nPlease provide value:".format(p))
    return 'conversation_set_param'

def set_param(bot, update, user_data):
    p_val = update.message.text
    p = user_data['cur_param']
    user_data['params'][p] = p_val
    logging.debug(u">>> Setting {} to {}".format(p, p_val))
    del user_data['cur_param']
    params = user_data['params']
    markup = ReplyKeyboardMarkup([params.keys()],
one_time_keyboard=True)
    update.message.reply_text(u"[set_param] Current parameters: \
{}".format([params]), disable_web_page_preview=True)
    update.message.reply_text('Choose param to set (or /done):', reply_markup=markup)
    return 'conversation_choose_param'

def render_template(bot, update, user_data):
    t = user_data['template']
    params = user_data['params']
    logging.info(u"Rendering template with {}".format(params))
    update.message.reply_text(t.get_template(params),
disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logging.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

start_handler = CommandHandler('start', start)
conv_handler = ConversationHandler(
    entry_points=[start_handler],
    states = {
        'conversation_got_template': [MessageHandler(Filters.text,
                                                     process_template, pass_user_data=True)],
        'conversation_process_params': [MessageHandler(Filters.text,
                                                       process_params,
                                                       pass_user_data=True),
                                       CommandHandler('done', render_template,
                                                      pass_user_data=True)],
        'conversation_choose_param': [MessageHandler(Filters.text,
                                                     choose_param, pass_user_data=True),
                                      CommandHandler('done', render_template,
                                                     pass_user_data=True)],
        'conversation_set_param': [MessageHandler(Filters.text,
                                                     set_param, pass_user_data=True),
                                   CommandHandler('done', render_template,
                                                  pass_user_data=True)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
dispatcher.add_handler(conv_handler)

updater.start_webhook('127.0.0.1', 7771, clean=True, webhook_url='https://bots.serverissues.com/tgposts-templates/')
updater.idle()
