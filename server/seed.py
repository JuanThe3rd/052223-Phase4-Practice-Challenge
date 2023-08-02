#!/usr/bin/env python3

import csv
from random import randint

from app import app
from models import db, Episode, Guest, Appearance

def clear_database():
    with app.app_context():
        Episode.query.delete()
        Guest.query.delete()
        Appearance.query.delete()
        db.session.commit()

def create_episodes(rows):
    with app.app_context():
        episodes = []
        for i in range(1, len(rows)):
            e = Episode(date=rows[i][2], number=i)
            episodes.append(e)
        db.session.add_all(episodes)
        db.session.commit()
    return episodes

def create_guests(rows):
    with app.app_context():
        guests = []
        for i in range(1, len(rows)):
            g = Guest(name=rows[i][-1], occupation=rows[i][1])
            guests.append(g)
        db.session.add_all(guests)
        db.session.commit()
    return guests

def create_appearances(rows, episodes, guests):
    with app.app_context():
        appearances = []
        for i in range(1, len(rows)):
            guest=Guest.query.filter(Guest.name==rows[i][-1]).first()
            episode=Episode.query.filter(Episode.date==rows[i][2]).first()
            a = Appearance(
                rating=randint(1, 5),
                guest_id = guest.id,
                episode_id = episode.id
            )
            appearances.append(a)
        db.session.add_all(appearances)
        db.session.commit()


if __name__ == '__main__':

    print("Clearing database...")
    clear_database()

    print("Opening CSV...")
    with open('./seed.csv', newline='') as csvfile:
        rows = [row for row in csv.reader(csvfile, delimiter=',', quotechar='|')]
        print("Seeding episodes...")
        episodes = create_episodes(rows)
        print("Seeding guests...")
        guests = create_guests(rows)
        print("Seeding appearances...")
        create_appearances(rows, episodes, guests)
        print("Complete!")
