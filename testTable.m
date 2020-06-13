function [adj,fix] = testTable()
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
adj.G = [0 1; 1 0]
adj.R = [1 0; 0 1]
adj.H = [1 0; 0 1]

fix.G = [0 0; 1 0]
fix.R = [1 0; 0 1]
fix.H = [1 0; 0 1]
end

