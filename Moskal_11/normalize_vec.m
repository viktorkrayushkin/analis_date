function [out] = normalize_vec(in)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
out = in - min(in);
out = out / max(out);
end

