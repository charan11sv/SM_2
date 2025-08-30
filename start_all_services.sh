#!/bin/bash

echo "Starting all microservices for Phase 1 testing..."
echo

echo "Starting Login Service (Port 8000)..."
gnome-terminal --title="Login Service" -- bash -c "cd login && docker-compose up --build; exec bash" &

echo "Starting Profile Service (Port 8001)..."
gnome-terminal --title="Profile Service" -- bash -c "cd profile-service && docker-compose up --build; exec bash" &

echo "Starting Posts Service (Port 8002)..."
gnome-terminal --title="Posts Service" -- bash -c "cd posts-service && docker-compose up --build; exec bash" &

echo "Starting Likes Service (Port 8003)..."
gnome-terminal --title="Likes Service" -- bash -c "cd likes-service && docker-compose up --build; exec bash" &

echo "Starting Comments Service (Port 8004)..."
gnome-terminal --title="Comments Service" -- bash -c "cd comments-service && docker-compose up --build; exec bash" &

echo
echo "All services are starting up..."
echo "Wait for all services to be ready, then run: python test_phase1_integration.py"
echo
read -p "Press Enter to continue..."
