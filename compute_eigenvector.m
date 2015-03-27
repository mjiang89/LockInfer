% Copyright by Meng Jiang
% Compute eigenvectors with adjacency matrix.
function [] = compute_eigenvector(graphfilename,ufilename,vfilename)
    k = 5;
    B = load(graphfilename);
    B = B+ones(size(B));
    i = B(:,1);
    j = B(:,2);
    s = ones(size(i));
    m = max(i);
    n = max(j);
    A = sparse(i,j,s,m,n);
    [U,S,V] = svds(A,k);
    for i = 1:k
        if sum(U(:,i)) < 0
            U(:,i) = -U(:,i);
        end
        if sum(V(:,i)) < 0
            V(:,i) = -V(:,i);
        end
    end
    dlmwrite(ufilename,U,'delimiter',',','precision',5);
    dlmwrite(vfilename,V,'delimiter',',','precision',5);  
end